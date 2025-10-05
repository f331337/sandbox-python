NUMBERS = [2139079, 1214759, 1516637, 1852285]


def factorize(number):
    for i in range(1, number + 1):
        if number % 1 == 0:
            yield i
