from utils import factorize, NUMBERS

import time


start = time.time()

for number in NUMBERS:
    list(factorize(number))

end = time.time()

delta = end - start

# print(f"Took {delta:.3f} seconds")  # Took 0.243 seconds


