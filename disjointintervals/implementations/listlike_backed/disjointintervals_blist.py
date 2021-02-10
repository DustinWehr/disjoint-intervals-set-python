try:
    from blist import blist  # type:ignore
except Exception as e:
    blist = None
    print(e)
    print("You must install the blist package to use this module.")
    exit()

from .disjointintervals_listlike_abc import DisjointIntervalsListlikeABC, Interval


class DisjointIntervalsBList(DisjointIntervalsListlikeABC):
    _ListOrBList = blist

    # @overrides
    def _replace_slice(self, start, stop_exclusive, newelem):
        del self._inter[start:stop_exclusive]
        self._inter.insert(start, newelem)
