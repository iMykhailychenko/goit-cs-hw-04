import time
from multiprocessing import Manager, Process
from queue import Queue
from threading import Thread

from utils import seed


def search_in_file(file_path, keywords, results):
    found = {}
    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            for keyword in keywords:
                if keyword in line:
                    found.setdefault(keyword, []).append((file_path, line_number))
    results.put(found)


def process_files_threading(file_list, keywords):
    results = Queue()
    threads = []

    for file_path in file_list:
        thread = Thread(target=search_in_file, args=(file_path, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    search_results = {}
    while not results.empty():
        found = results.get()
        for keyword, occurrences in found.items():
            search_results.setdefault(keyword, []).extend(occurrences)

    return search_results


def process_files_multiprocessing(file_list, keywords):
    with Manager() as manager:
        results = manager.Queue()
        processes = []

        for file_path in file_list:
            process = Process(
                target=search_in_file, args=(file_path, keywords, results)
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        search_results = {}
        while not results.empty():
            found = results.get()
            for keyword, occurrences in found.items():
                search_results.setdefault(keyword, []).extend(occurrences)

    return search_results


if __name__ == "__main__":
    files = ["./assets/file1.txt", "./assets/file2.txt", "./assets/file3.txt"]
    keywords = [
        "keyword1",
        "keyword2",
        "keyword3",
    ]
    seed(files, keywords)

    # Багатопотоковий підхід
    print("Threading approach:")
    start_time_threading = time.time()
    threading_results = process_files_threading(files, keywords)
    end_time_threading = time.time()
    print("Results:", threading_results)
    print("Execution time:", end_time_threading - start_time_threading, "seconds")

    # Багатопроцесорний підхід
    print("\nMultiprocessing approach:")
    start_time_multiprocessing = time.time()
    multiprocessing_results = process_files_multiprocessing(files, keywords)
    end_time_multiprocessing = time.time()

    print("Results:", multiprocessing_results)
    print(
        "Execution time:",
        end_time_multiprocessing - start_time_multiprocessing,
        "seconds",
    )
