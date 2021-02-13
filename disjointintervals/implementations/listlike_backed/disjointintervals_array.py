from typing import Any, Tuple, List, Iterable

from .disjointintervals_listlike_abc import DisjointIntervalsListlikeABC
from array import array
from bisect import bisect_left, bisect_right

from ..interval_util import packed_intersection_nonempty

IntInterval = int  # actually, 64-bit int

class DisjointIntervalsArray(DisjointIntervalsListlikeABC):
    def _listlist_constructor(self, itemsiter: Iterable[Tuple[int,int]]) -> Any:
        return array("q", [self._pair_interval_to_int(x) for x in itemsiter])

    def _internal_listlist_constructor(self, itemsiter: Iterable[int]) -> Any:
        return array("q", itemsiter)

    def _sort(self) -> None:
        """quick and dirty"""
        as_list = list(self._inter)
        as_list.sort(key=lambda x: self._interval_to_left_endpoint(x))
        for i in range(len(self)):
            self._inter[i] = as_list[i]

    def intervals(self) -> List[Tuple[int, int]]:
        return [(self._interval_to_left_endpoint(I), self._interval_to_right_endpoint(I)) for I in self._inter]

    def _unpack_interval(self, i: int) -> Tuple[int,int]:
        x = self._inter[i]
        return x >> 32, x & 0b0000000000000000000000000000000011111111111111111111111111111111
    def _pair_interval_to_int(self, pair: Tuple[int,int]) -> int:
        return self._interval(pair[0], pair[1])
    def _int_interval_to_pair(self, x: int) -> Tuple[int,int]:
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

    def _replace_slice(self, start, stop_exclusive, newelem):
        self._inter[start:stop_exclusive] = self._internal_listlist_constructor([newelem])

    def _bisect_left(self, x: int):
        return bisect_left(self._inter, x << 32)

    def _bisect_right(self, x: int):
        return bisect_right(self._inter, x << 32)

    def _intersection_nonempty(self, r1, r2) -> bool:
        return packed_intersection_nonempty(r1, r2)

    def get_intersecting(self, s: int, e: int) -> List[Tuple[int,int]]:
        return [self._int_interval_to_pair(x) for x in super().get_intersecting(s, e)]