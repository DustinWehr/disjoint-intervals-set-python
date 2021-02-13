from sys import argv

if "profile" in argv:
    import cProfile

assert False, "Please run this with python's -O flag, as the code has many inefficient assert statements."

skip_blist = False
try:
    from blist import blist  # type:ignore
    from DisjointIntervalsSet.disjointintervals.implementations.listlike_backed \
        .disjointintervals_blist import DisjointIntervalsBList
except Exception as e:
    print("Skipping performance test for blist-based implementation, since it's not installed.")
    skip_blist = True

from DisjointIntervalsSet.disjointintervals.implementations.listlike_backed\
    .disjointintervals_list import DisjointIntervalsList
from DisjointIntervalsSet.disjointintervals.implementations.listlike_backed\
    .disjointintervals_array import DisjointIntervalsArray
from DisjointIntervalsSet.disjointintervals.implementations.slow_for_specification_only\
    .disjointintervals_specification import DisjointIntervalsSlowSpec


from DisjointIntervalsSet.tests.helpers_for_tests import run_ops_timed

print("""Run this script with one of
> python3 -O DisjointIntervalsSet/tests/compare_performance.py
> pypy3 -O DisjointIntervalsSet/tests/compare_performance.py
(or whatever your python 3.x cpython or pypy executable is called)
""")

from DisjointIntervalsSet.tests.helpers_for_tests import random_adds_various_deletes

if __name__ == '__main__':
    # ops1 = random_adds_various_deletes(1000000, .7, range(0, 100000000), 100, 10000)
    # ops1b = random_adds_various_deletes(100000, .9, range(0, 1000000000), 100, 1000000)
    # ops1c = random_adds_various_deletes(500000, .8, range(0, 100000000), 100, 10000)
    ops1 = random_adds_various_deletes(1000000, .7, range(0, 100000000), 10, 50)

    # ops2 = random_adds_various_deletes(100000, .8, range(0, 1000000), 1000, 100000)
    # ops3 = random_adds_various_deletes(100000, .8, range(0, 100000), 100, 10000)
    # ops4 = random_adds_various_deletes(100000, .8, range(0, 1000000), 100, 10000)

    opseq_to_use = ops1

    rspec = DisjointIntervalsSlowSpec()
    rlist = DisjointIntervalsList()
    rarray = DisjointIntervalsArray()
    if not skip_blist:
        rblist = DisjointIntervalsBList()

    # rspec takes too long on ops1
    # cProfile.run("run_ops_timed(rspec, ops1)", sort=1)

    print("Testing array-based implementation")
    run_ops_timed(rarray, opseq_to_use)
    print("Testing list-based implementation")
    run_ops_timed(rlist, opseq_to_use)
    if not skip_blist:
        print("Testing blist-based implementation")
        run_ops_timed(rblist, opseq_to_use)

    if "profile" in argv:
        print("Now running same tests with cProfile.")
        cProfile.run("run_ops_timed(rlist, opseq_to_use)", sort=1)
        if not skip_blist:
            cProfile.run("run_ops_timed(rblist, opseq_to_use)", sort=1)
