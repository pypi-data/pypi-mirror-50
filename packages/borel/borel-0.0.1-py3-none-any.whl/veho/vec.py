def ini(size, ject_value):
    return [ject_value(i) for i in range(size)]


def is_empty(arr: list):
    if arr:
        return True
    else:
        return False


def zips(*arr_list, zipper):
    tups = zip(*arr_list)
    return [zipper(*tup) for tup in tups]


def distinct(arr: list):
    return list(dict.fromkeys(arr))


def progression(size, initial, progress):
    return list(range(initial, initial + size * progress, progress))
