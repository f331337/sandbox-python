import csv
from time import time

from pydantic import BaseModel


class TransactionRow(BaseModel):
    TransactionId: str
    TransactionType: str
    Product: str


def main():
    with open("out.csv", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        counter = 0

        for row in csv_reader:
            _ = TransactionRow.model_validate(row)
            counter += 1
        print(counter)


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    delta = end - start
    print(f"delta {delta} seconds")
