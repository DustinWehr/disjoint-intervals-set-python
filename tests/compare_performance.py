from blist import blist
import cProfile

print("""Run this script with one of
> python3 -O tests/compare_performance.py
> pypy3 -O tests/compare_performance.py
(or whatever your python 3.x cpython or pypy executable is called)
""")

from tests.helpers_for_tests import *
from tests.helpers_for_tests import run_ops_timed

if __name__ == '__main__':
    # for showing better perf by blist:
    ops1 = random_adds_various_deletes(100000, .9, range(0, 100000000), 1000, 10000)
    ops1a = random_adds_various_deletes(100000, .8, range(0, 100000000), 1000, 10000)

    ops2 = random_adds_various_deletes(100000, .8, range(0, 1000000), 1000, 100000)
    ops3 = random_adds_various_deletes(100000, .8, range(0, 100000), 100, 10000)
    ops4 = random_adds_various_deletes(100000, .8, range(0, 1000000), 100, 10000)

    rspec = DisjointIntervalsSlowSpec()
    rarray = DisjointIntervalsList()
    rblist = DisjointIntervalsBList()
    rsortedlist = DisjointIntervalsSortedList([])

    # rspec takes too long on ops1
    # cProfile.run("run_ops_timed(rspec, ops1)", sort=1)
    cProfile.run("run_ops_timed(rarray, ops1)", sort=1)
    cProfile.run("run_ops_timed(rblist, ops1)", sort=1)
    # cProfile.run("run_ops_timed(rsortedlist, ops1)", sort=1)
