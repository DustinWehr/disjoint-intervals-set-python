from typing import List, Iterable, Tuple

Interval = Tuple[int, int]


class DisjointIntervalsInterface:
    def __init__(self, intervals: Iterable[Interval] = None) -> None:
        pass

    def __eq__(self, other) -> bool:
        return self.intervals() == other.intervals()

    def __str__(self) -> str:
        intervals = self.intervals()
        if len(intervals) == 0:
            return "{}"
        return ", ".join(f"[{I[0]},{I[1]})" for I in intervals)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        raise NotImplementedError

    def intervals(self) -> List[Interval]:
        pass

    def add(self, start: int, end: int) -> None:
        pass

    def delete(self, start: int, end: int) -> None:
        pass

    def get_intersecting(self, start: int, end: int) -> List[Interval]:
        pass

