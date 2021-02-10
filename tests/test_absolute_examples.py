from .helpers_for_tests import run_ops, allimpl, run_ops_parallel_compare_many

# allimpl makes the test run against all the DisjointIntervalsInterface implementations enabled in
# src/helpers_for_tests.py


@allimpl
def test_empty_add(C=None):
    state = C([])
    state.delete(1, 2)
    assert state == C([])
    state.add(1, 2)
    assert state == C([(1, 2)])


@allimpl
def test_empty(C=None):
    state = C([])
    state.delete(1, 2)
    assert state == C([])
    state.add(1, 2)
    assert state == C([(1, 2)])


@allimpl
def test_add_no_overlap(C=None):
    state = C([(1, 2)])
    state.add(3, 5)
    assert state == C([(1, 2), (3, 5)])


@allimpl
def test_add_full_overlap(C=None):
    state = C([(1, 6)])
    state.add(3, 5)
    assert state == C([(1, 6)])


@allimpl
def test_add_partial_overlap(C=None):
    state = C([(1, 4)])
    state.add(3, 5)
    assert state == C([(1, 5)])


@allimpl
def test_add_larger(C=None):
    state = C([(1, 4), (6, 20), (30, 40)])
    state.add(18, 35)
    assert state == C([(1, 4), (6, 40)])


@allimpl
def test_add_join(C=None):
    state = C([(1, 2)])
    state.add(2, 3)
    assert state == C([(1, 3)])


@allimpl
def test_add_join0(C=None):
    state = C([(1, 2)])
    state.add(0, 1)
    assert state == C([(0, 2)])


@allimpl
def test_add_join2(C=None):
    state = C([(-10, -5), (10, 20), (100, 101)])
    state.add(1, 2)
    state.add(10, 20)
    state.add(2, 3)
    assert state == C([(-10, -5), (1, 3), (10, 20), (100, 101)])


@allimpl
def test_add_join3(C=None):
    state = C([])
    state.add(4, 5)
    state.add(1, 2)
    state.add(5, 6)
    assert state == C([(1, 2), (4, 6)])


@allimpl
def test_add_confused(C=None):
    state = C([])
    state.add(2, 3)
    state.add(3, 4)
    state.add(5, 6)
    assert state == C([(2, 4), (5, 6)])


@allimpl
def test_add_from_rand(C=None):
    state = C([(10, 20), (30, 40)])
    state.add(25, 35)
    assert state == C([(10, 20), (25, 40)])

    state = C([(30, 40), (10, 20)])
    state.add(25, 35)
    assert state == C([(10, 20), (25, 40)])

    state = C([(15109, 15939), (17245, 18000)])
    state.delete(8974, 15109)
    state.add(16805, 17253)
    assert state == C([(15109, 15939), (16805, 18000)])


@allimpl
def test_delete_no_overlap(C=None):
    state = C([(1, 6)])
    state.delete(-3, -1)
    assert state == C([(1, 6)])


@allimpl
def test_delete_full_overlap(C=None):
    state = C([(1, 6)])
    state.delete(-1, 10)
    assert state == C([])


@allimpl
def test_delete_partial_overlap(C=None):
    state = C([(1, 6)])
    state.delete(4, 10)
    assert state == C([(1, 4)])


@allimpl
def test_delete_split(C=None):
    state = C([(1, 6)])
    state.delete(3, 4)
    assert state == C([(1, 3), (4, 6)])


@allimpl
def test_delete_from_rand(C=None):
    state = C([(10, 40), (50, 60)])
    state.delete(20, 30)
    assert state == C([(10, 20), (30, 40), (50, 60)])


@allimpl
def test_delete_many(C=None):
    state = C([])
    state.add(0, 30)
    state.delete(-10, 2)
    state.delete(5, 8)
    state.delete(2, 3)
    state.delete(25, 35)
    assert state == C([(3, 5), (8, 25)])


@allimpl
def test_delete_first_el(C=None):
    state = C([])
    state.add(0, 30)
    state.delete(0, 1)
    assert state == C([(1, 30)])


@allimpl
def test_delete_last_el(C=None):
    state = C([])
    state.add(0, 30)
    state.delete(29, 30)
    assert state == C([(0, 29)])


@allimpl
def test_delete_last_el_overlap(C=None):
    state = C([])
    state.add(0, 30)
    state.delete(29, 35)
    assert state == C([(0, 29)])


@allimpl
def test_add_delete_misc(C=None):
    state = C([])
    state.add(-5, 5)
    state.add(10, 15)
    state.add(8, 15)
    assert state == C([(-5, 5), (8, 15)])
    state.delete(10, 11)
    assert state == C([(-5, 5), (8, 10), (11, 15)])
    state.delete(-100, 100)
    assert state == C([])


@allimpl
def test_bleh(C=None):
    state = C([])
    state.add(-5, 5)
    state.add(10, 15)
    assert state == C([(-5, 5), (10, 15)])
    state.add(7, 11)
    assert state == C([(-5, 5), (7, 15)])
    state.delete(-100, 100)
    assert state == C([])


@allimpl
def test_get_no_overlap(C=None):
    state = C([(1, 3), (5, 7)])
    assert state.get_intersecting(4, 5) == C([]).intervals()


@allimpl
def test_get_partial_overlap1(C=None):
    state = C([(1, 3), (5, 6)])
    assert state.get_intersecting(4, 6) == C([(5, 6)]).intervals()


@allimpl
def test_get_all_hit(C=None):
    state = C([(1, 3), (5, 6)])
    assert state.get_intersecting(2, 9) == C([(1, 3), (5, 6)]).intervals()


@allimpl
def test_ops_ellusive(C=None):
    state = C()
    ops = [('a', (3266, 3621)), ('a', (17245, 18000)), ('a', (3800, 4770)), ('d', (3366, 9057)), ('d', (6069, 10404)), ('a', (15035, 15939)),
           ('a', (3148, 3730)), ('d', (8241, 11996)), ('a', (11841, 11869)), ('d', (2581, 7810)), ('d', (8974, 15109)), ('a', (16805, 17253))]
    run_ops(state, ops)
    assert state.intervals() == [(15109, 15939), (16805, 18000)]


def test_ops_ellusive_parallel():
    ops = [('a', (3266, 3621)), ('a', (17245, 18000)), ('a', (3800, 4770)), ('d', (3366, 9057)), ('d', (6069, 10404)), ('a', (15035, 15939)),
           ('a', (3148, 3730)), ('d', (8241, 11996)), ('a', (11841, 11869)), ('d', (2581, 7810)), ('d', (8974, 15109)), ('a', (16805, 17253))]
    run_ops_parallel_compare_many(ops)
