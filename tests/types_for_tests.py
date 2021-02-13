from typing import List, Iterable, NamedTuple, Tuple
from DisjointIntervalsSet.disjointintervals.types.disjointintervals import TupInterval

RangeOp = Tuple[str, TupInterval] # str part is 'a' (add), 'd' (delete), or 'g' (get).
# alternative, which I had some reason not to use:
# class RangeOp(NamedTuple):
#     optype: str # a,d, or g
#     arg: Interval

RangeOpSeq = List[RangeOp]


class ATestCase(NamedTuple):
    """
    pytest didn't like it starting with Test so I added the arbitrary letter A.
    """
    opseq: RangeOpSeq
    expected: Iterable[TupInterval]
