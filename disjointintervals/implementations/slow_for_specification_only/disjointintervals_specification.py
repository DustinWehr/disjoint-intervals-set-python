from typing import Iterable, List


from DisjointIntervalsSet.disjointintervals.implementations.interval_util import *
from DisjointIntervalsSet.disjointintervals.types.disjointintervals import DisjointIntervalsInterface
from DisjointIntervalsSet.disjointintervals.types.disjointintervals import Interval


class DisjointIntervalsSlowSpec(DisjointIntervalsInterface):
    def __init__(self, intervals: Iterable[Interval] = None) -> None:
        DisjointIntervalsInterface.__init__(self)
        self._intervals = list(intervals) if intervals else []

    def intervals(self) -> List[Interval]:
        return self._intervals

    def add(self, start: int, end: int) -> None:
        new_intervals: List[Interval] = []
        r1 = (start, end)
        accumulated = r1
        for r2 in self._intervals:
            if separated(r1, r2):
                # the intervals that don't merge with r1
                new_intervals.append(r2)
            else:
                # the intervals that merge with r1
                accumulated = union(accumulated, r2)
        new_intervals.append(accumulated)
        new_intervals.sort()  # just to put accumulated in the correct spot
        self._intervals = new_intervals

    def delete(self, start: int, end: int) -> None:
        new_intervals: List[Interval] = []
        r1 = (start, end)
        for r2 in self._intervals:
            # difference returns 0, 1 or 2 nonempty ranges.
            ranges = difference(r2, r1)
            for r in ranges:
                assert nonempty(r)
            new_intervals.extend(ranges)
        new_intervals.sort()
        self._intervals = new_intervals

    def get_intersecting(self, start: int, end: int) -> List[Interval]:
        rv: List[Interval] = []
        r1 = (start, end)
        for r2 in self._intervals:
            if intersection_nonempty(r1, r2):
                rv.append(r2)
        return rv

    def __len__(self) -> int:
        return len(self._intervals)
