import time
from threading import Thread
from utils import factorize, NUMBERS


class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time.time()

threads = []
for number in NUMBERS:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start

print(f"Took {delta:.3f} seconds")  # Took
