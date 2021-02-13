from typing import List, Iterable, Tuple, Any, TypeVar

Interval = Any
TupInterval = Tuple[int, int]
I = TypeVar("I")

class DisjointIntervalsInterface:
    def __init__(self) -> None:
        pass

    def _listlist_constructor(self, itemsiter: Iterable[TupInterval]) -> Any:
        pass

    def __eq__(self, other) -> bool:
        return self.intervals() == other.intervals()

    def __str__(self) -> str:
        intervals = self.intervals()
        if len(intervals) == 0:
            return "{}"
        return ", ".join(f"[{inter[0]},{inter[1]})" for inter in intervals)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        raise NotImplementedError

    def intervals(self) -> List[TupInterval]:
        pass

    def add(self, start: int, end: int) -> None:
        pass

    def delete(self, start: int, end: int) -> None:
        pass

    def get_intersecting(self, start: int, end: int) -> List[TupInterval]:
        pass

