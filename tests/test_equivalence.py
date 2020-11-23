from blist import blist

# from disjointintervals.DisjointIntervalsParametric import DisjointIntervalsParametric
from .context import disjointintervals
# from disjointintervals.disjointintervals_slow4spec import DisjointIntervalsSlowSpec
# from disjointintervals.disjointintervals_fast import DisjointIntervalsFast
from .helpers_for_tests import *

def mk_blist_intervals():
    return DisjointIntervalsFast([], blist)

def test_random_ops2():
    ops = random_adds_various_deletes(100000, .6, range(0, 1000), 1000, 1000)
    run_ops_parallel_compare_many(
        ops, [DisjointIntervalsSlowSpec,
              DisjointIntervalsFast,  # default uses list
              mk_blist_intervals,
              # DisjointIntervalsSortedList
              # DisjointIntervalsSortedContainers
              # DisjointIntervalsParametric])
             ])

def test_random_ops():
    ops = random_adds_various_deletes(100000, .8, range(0, 100000), 10000, 10000)
    run_ops_parallel_compare_many(
        ops, [DisjointIntervalsSlowSpec,
              DisjointIntervalsFast,  # default uses list
              mk_blist_intervals,
              # DisjointIntervalsSortedList
              # DisjointIntervalsSortedContainers
              # DisjointIntervalsParametric
              ])



