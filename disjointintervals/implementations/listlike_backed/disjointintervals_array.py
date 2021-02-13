from ctypes import Array
from typing import Any, Tuple, List, Iterable

from DisjointIntervalsSet.disjointintervals.types.disjointintervals import TupInterval
from .disjointintervals_listlike_abc import DisjointIntervalsListlikeABC
from array import array
from bisect import bisect_left, bisect_right

from ..interval_util import intersection_nonempty

IntInterval = int  # actually, 64-bit int


def packed_to_pair(x: IntInterval) -> TupInterval:
    return x >> 32, x & 0b0000000000000000000000000000000011111111111111111111111111111111

def packed_intersection_nonempty(r1: int, r2: int) -> bool:
    return intersection_nonempty(packed_to_pair(r1), packed_to_pair(r2))


class DisjointIntervalsArray(DisjointIntervalsListlikeABC):
    def _listlist_constructor(self, itemsiter: Iterable[TupInterval]) -> array[IntInterval]:
        return array("Q", [self._pair_interval_to_int(x) for x in itemsiter])

    def _internal_listlist_constructor(self, itemsiter: Iterable[IntInterval]) -> array[IntInterval]:
        return array("q", itemsiter)

    def _sort(self) -> None:
        """quick and dirty"""
        as_list = list(self._inter)
        as_list.sort(key=lambda x: self._interval_to_left_endpoint(x))
        for i in range(len(self)):
            self._inter[i] = as_list[i]

    def intervals(self) -> List[TupInterval]:
        return [(self._interval_to_left_endpoint(I), self._interval_to_right_endpoint(I)) for I in self._inter]

    def _get_unpack_interval(self, i: int) -> TupInterval:
        x = self._inter[i]
        return x >> 32, x & 0b0000000000000000000000000000000011111111111111111111111111111111
    def _pair_interval_to_int(self, pair: TupInterval) -> IntInterval:
        return self._interval(pair[0], pair[1])
    def _int_interval_to_pair(self, x: IntInterval) -> TupInterval:
        return self._interval_to_left_endpoint(x), self._interval_to_right_endpoint(x)
    def _interval(self, left, right):
        return (left << 32) + right
    def _interval_to_left_endpoint(self, interval: IntInterval) -> int:
        return interval >> 32
    def _interval_to_right_endpoint(self, interval: IntInterval) -> int:
        return interval & 0b0000000000000000000000000000000011111111111111111111111111111111
    def _get_left_endpoint(self, i):
        return self._inter[i] >> 32
    def _get_right_endpoint(self, i):
        return self._inter[i] & 0b0000000000000000000000000000000011111111111111111111111111111111

    def _replace_slice(self, start: int, stop_exclusive: int, newelem: IntInterval):
        self._inter[start:stop_exclusive] = self._internal_listlist_constructor([newelem])

    def _bisect_left(self, x: IntInterval) -> int:
        return bisect_left(self._inter, x << 32)

    def _bisect_right(self, x: IntInterval) -> int:
        return bisect_right(self._inter, x << 32)

    def _intersection_nonempty(self, r1, r2) -> bool:
        return packed_intersection_nonempty(r1, r2)

    def get_intersecting(self, s: int, e: int) -> List[TupInterval]:
        return [self._int_interval_to_pair(x) for x in super().get_intersecting(s, e)]