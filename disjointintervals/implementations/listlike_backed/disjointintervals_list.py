from typing import Any
from .disjointintervals_listlike_abc import DisjointIntervalsListlikeABC

class DisjointIntervalsList(DisjointIntervalsListlikeABC):
    def _listlist_constructor(self, itemsiter) -> Any:
        return list(itemsiter)
