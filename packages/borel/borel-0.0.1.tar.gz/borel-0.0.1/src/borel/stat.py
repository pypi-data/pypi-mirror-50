from typing import Tuple


def cnt(arr: list):
    return len(arr)


def avg(arr: list):
    if arr:
        return sum(arr) / len(arr)
    else:
        return 0


def bound(arr: list) -> Tuple[int or float, int or float]:
    """
    :return Tuple[max, min]
    """
    if arr:
        pk, vl = arr[0], arr[0]
        for x in arr:
            if x > pk:
                pk = x
            if x < vl:
                vl = x
        return pk, vl
    else:
        return None, None
