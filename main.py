import time
from multiprocessing import Manager, Process
from multiprocessing import RLock as MpLock
from queue import Queue
from threading import RLock as ThLock
from threading import Thread

from utils import seed


def search_in_file(path: str, keywords: list[str], locker, results: dict):
    try:
        with locker, open(path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                for keyword in keywords:
                    index = line.find(keyword)
                    if index > 0:
                        results[keyword].append(
                            f'"{keyword}" found at {line_number}:{index}'
                        )
    except Exception:
        print("Error while reading file: ", path)


def with_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Execution time:", end_time - start_time, "seconds")
        print("Results:", result)
        return result

    return wrapper


@with_timer
def process_files_threading(file_list, keywords):
    lock = ThLock()
    threads = []
    results = {keyword: [] for keyword in keywords}
    for file in file_list:
        th = Thread(target=search_in_file, args=(file, keywords, lock, results))
        th.start()
        threads.append(th)
    [th.join() for th in threads]
    return results


@with_timer
def process_files_multiprocessing(file_list, keywords):
    lock = MpLock()
    processes = []
    with Manager() as manager:
        results = manager.dict({keyword: manager.list() for keyword in keywords})
        for file in file_list:
            p = Process(target=search_in_file, args=(file, keywords, lock, results))
            p.start()
            processes.append(p)
        [process.join() for process in processes]
        return { keyword: list(result) for keyword, result in results.items() }


if __name__ == "__main__":
    files = ["./assets/file1.txt", "./assets/file2.txt", "./assets/file3.txt"]
    keywords = ["keyword1", "keyword2", "keyword3"]
    seed(files, keywords)

    # Багатопотоковий підхід
    print("Threading approach:")
    process_files_threading(files, keywords)

    # Багатопроцесорний підхід
    print("\nMultiprocessing approach:")
    process_files_multiprocessing(files, keywords)
