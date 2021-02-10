from DisjointIntervalsSet.disjointintervals.implementations.slow_for_specification_only.disjointintervals_specification import DisjointIntervalsSlowSpec
from DisjointIntervalsSet.disjointintervals.implementations.listlike_backed.disjointintervals_list import DisjointIntervalsList
from DisjointIntervalsSet.disjointintervals.implementations.listlike_backed.disjointintervals_blist import DisjointIntervalsBList
from .helpers_for_tests import run_ops

# will be called by pytest
def test_small_opseq(opseq):
    ranges_spec = DisjointIntervalsSlowSpec()
    run_ops(ranges_spec, opseq)

    ranges_list = DisjointIntervalsList()
    ranges_blist = DisjointIntervalsBList()

    # The following two run_ops/assert commands should be in different test cases, but
    # I didn't take the time to figure out how to do that with pytest.

    run_ops(ranges_list, opseq)
    assert ranges_spec == ranges_list

    run_ops(ranges_blist, opseq)
    assert ranges_spec == ranges_blist
