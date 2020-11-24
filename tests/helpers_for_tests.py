import time
from functools import update_wrapper
from typing import List, Tuple, cast, Type, Set
from random import random as rand01
import random

from .context import disjointintervals
from disjointintervals.types.disjointintervals import Interval
from disjointintervals.types.disjointintervals import DisjointIntervalsInterface
from disjointintervals.disjointintervals_slow4spec import DisjointIntervalsSlowSpec
from disjointintervals.disjointintervals_list import DisjointIntervalsList
from disjointintervals.disjointintervals_blist import DisjointIntervalsBList
from disjointintervals.disjointintervals_blistsortedlist import DisjointIntervalsSortedList

RangeOp = Tuple[str, Interval]

# random.seed(10202)

IMPLEMENTATIONS = [DisjointIntervalsSlowSpec,
                   DisjointIntervalsList,
                   DisjointIntervalsBList,
                   # DisjointIntervalsSortedList
                   ]

SIZE_CHANGE_NOTIF_THRESH = 1000
SIZE_INC_NOTIF_THRESH = 1000

def allimpl(fn):
    def test_it():
        for C in IMPLEMENTATIONS:
            print(f"{fn.__name__} with {C.__name__}")
            fn(C)
    update_wrapper(test_it, fn)
    return test_it


def op2str(op: RangeOp):
    if op[0] == 'a':
        return f"Add [{op[1][0]},{op[1][1]})"
    if op[0] == 'd':
        return f"Delete [{op[1][0]},{op[1][1]})"
    if op[0] == 'g':
        return f"Get [{op[1][0]},{op[1][1]})"


def run_ops(ranges: DisjointIntervalsInterface,
            ops: List[RangeOp]) -> None:
    for op in ops:
        run_op(ranges, op)
        # if "_start" in dir(ranges):
        #     print(op)
        #     print(ranges)
        #     print(ranges._start)


def run_op(ranges: DisjointIntervalsInterface, op: RangeOp) -> None:
    if op[0] == 'a':
        ranges.add(op[1][0], op[1][1])
    elif op[0] == 'd':
        ranges.delete(op[1][0], op[1][1])
    else:
        assert op[0] == 'g'
        ranges.get_intersecting(op[1][0], op[1][1])


def run_ops_timed(ranges: DisjointIntervalsInterface,
                  ops: List[RangeOp]) -> None:
    start = time.perf_counter()
    cursize = 0
    last_inc_notif = 0
    for op in ops:
        run_op(ranges, op)
        newsize = len(ranges)
        if abs(newsize - last_inc_notif) > SIZE_CHANGE_NOTIF_THRESH:
            print(f"# intervals changed since last notification by {newsize - last_inc_notif} to {newsize}.")
            last_inc_notif = newsize
        # if abs(newsize - cursize) > SIZE_CHANGE_NOTIF_THRESH:
        #     print(f"# intervals changed in one op by {newsize - cursize} to {newsize}.")
        cursize = newsize
    print(f"{time.perf_counter() - start} seconds.")


def run_ops_parallel_compare_many(ops: List[RangeOp],
                                  classes: List[Type[DisjointIntervalsInterface]] = IMPLEMENTATIONS) -> None:
    versions = [C() for C in classes]
    for op in ops:
        print("\n" + op2str(op))

        for i, ds in enumerate(versions):
            run_op(ds, op)
            print(f"Alg {i + 1} yields : {ds}   ({classes[i].__name__})")

        for i in range(1, len(versions)):
            assert versions[0].intervals() == versions[i].intervals()


def random_adds_various_deletes(total_ops: int, add_probability: float,
                                element_range, max_add_size,
                                max_del_size) -> List[RangeOp]:
    ops = cast(List[RangeOp], [None] * total_ops)
    for i in range(total_ops):
        if rand01() < add_probability:
            x = random.choice(element_range)
            size = random.choice(range(1, max_add_size))
            ops[i] = ('a', (x, x + size))
        else:
            x = random.choice(element_range)
            size = random.choice(range(1, max_del_size))
            ops[i] = ('d', (x, x + size))
    return ops
