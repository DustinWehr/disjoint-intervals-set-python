from typing import List, Tuple


def bisect_left_py(a: List[Tuple[int, int]], x: int):
    """
    Note unlike functions from bisect package, this function assumes we are searching a list of tuples, and that the
    search is only based on the first element of the tuples.
    """
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid][0] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bisect_right_py(a, x: int):
    """
    See note in bisect_left
    """
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid][0]:
            hi = mid
        else:
            lo = mid + 1
    return lo
