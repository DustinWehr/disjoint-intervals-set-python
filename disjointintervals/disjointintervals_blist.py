from typing import Iterable
from bisect import bisect_right, bisect_left
from blist import blist

from disjointintervals.disjointintervals_listlike_abc import DisjointIntervalsListlikeABC, Interval

USE_CPYTHON_BISECT_WITH_BLIST = False


class DisjointIntervalsBList(DisjointIntervalsListlikeABC):
    _ListOrBList = blist

    def __init__(self, intervals: Iterable[Interval] = None):
        super().__init__(intervals)
        if USE_CPYTHON_BISECT_WITH_BLIST:
            self._bisect_left = lambda x: bisect_left(self._inter, (x, x))
            self._bisect_right = lambda x: bisect_right(self._inter, (x, x))

    # @overrides
    def _bisect_left(self, x: int):
        # This method gets overwritten if USE_CPYTHON_BISECT is True.
        # Next line would use CPython's bisect_left, which makes tests pass and is something like 10 or 20% faster,
        # but I have no idea why it appears to work with blist, and no confidence that it's actually correct to use it.
        # So, I've copied the python code from python 3.8's bisect.py into here instead. But you can override the use of
        # this by setting USE_CPYTHON_BISECT = True.
        # return bisect_left(self._inter, (x,x))
        a = self._inter
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid][0] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    # @overrides
    def _bisect_right(self, x: int):
        # See note in _bisect_left
        # return bisect_right(self._inter, (x,x))
        a = self._inter
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid][0]:
                hi = mid
            else:
                lo = mid + 1
        return lo
