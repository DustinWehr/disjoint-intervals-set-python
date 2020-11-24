from .helpers_for_tests import *

def test_random_ops2():
    ops = random_adds_various_deletes(100000, .6, range(0, 1000), 1000, 1000)
    run_ops_parallel_compare_many(ops, IMPLEMENTATIONS)

def test_random_ops():
    ops = random_adds_various_deletes(100000, .8, range(0, 100000), 10000, 10000)
    run_ops_parallel_compare_many(ops, IMPLEMENTATIONS)
