from .context import disjointintervals
from disjointintervals.disjointintervals_slow4spec import DisjointIntervalsSlowSpec
from disjointintervals.disjointintervals_blist_or_list import DisjointIntervalsList, DisjointIntervalsBList
from disjointintervals.disjointintervals_blist_sortedlist import DisjointIntervalsSortedList
from .helpers_for_tests import run_ops

def test_small_opseq(opseq):
    ranges_spec = DisjointIntervalsSlowSpec()
    run_ops(ranges_spec, opseq)

    ranges_array = DisjointIntervalsList()
    ranges_blist = DisjointIntervalsBList()
    ranges_sortedlist = DisjointIntervalsSortedList([])

    # The following two run_ops/assert commands should be in different test cases, but
    # I didn't take the time to figure out how to do that with pytest.

    run_ops(ranges_array, opseq)
    assert ranges_spec == ranges_array

    run_ops(ranges_blist, opseq)
    assert ranges_spec == ranges_blist

    # run_ops(ranges_spec, opseq)
    # assert ranges_spec == ranges_sortedlist
