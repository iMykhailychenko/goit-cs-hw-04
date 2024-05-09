import random

from faker import Faker

fake = Faker()


def seed(files, keywords):
    for idx, file in enumerate(files):
        with open(file, "w", encoding="utf-8") as f:
            keyword = keywords[idx]
            text = fake.text(max_nb_chars=10000)
            index = random.randint(0, len(text))
            text_with_keyword = f"{text[:index]} {keyword} {text[index:]}"
            f.write(text_with_keyword)
