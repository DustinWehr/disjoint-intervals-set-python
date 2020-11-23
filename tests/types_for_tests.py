from typing import List, Iterable, NamedTuple, Tuple

Interval = Tuple[int,int]

RangeOp = Tuple[str, Interval]
# class RangeOp(NamedTuple):
#     optype: str # a,d, or g
#     arg: Interval

RangeOpSeq = List[RangeOp]

class KTestCase(NamedTuple):
    """
    pytest didn't like it starting with Test so I added K.
    """
    opseq: RangeOpSeq
    expected: Iterable[Interval]

# KTestCase = Tuple[RangeOp, List[Interval]]