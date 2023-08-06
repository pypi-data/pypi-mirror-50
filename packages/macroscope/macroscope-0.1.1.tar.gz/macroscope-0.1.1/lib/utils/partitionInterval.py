from typing import List


def frange(start, stop, step):
    i = start
    while i <= stop:
        yield i
        i += step


def partitionInterval(a: float, b: float, k: int) -> List[float]:
    """
    a: start of interval
    b: end of interval
    k: number of items in partition
    """

    if a >= b:
        raise ValueError("Start of interval: " + a + " must be less than end of interval: " + b)

    if k < 2:
        k = 2

    step = (b - a)/(k - 1)

    return list(frange(a, b, step))
