from bisect import bisect_right, bisect_left

from disjointintervals.disjointintervals_listlike_abc import DisjointIntervalsListlikeABC


class DisjointIntervalsList(DisjointIntervalsListlikeABC):
    _ListOrBList = list

    # # @overrides
    # def _bisect_left(self, x: int):
    #     return bisect_left(self._inter, (x, x))
    #
    # # @overrides
    # def _bisect_right(self, x: int):
    #     return bisect_right(self._inter, (x, x))
