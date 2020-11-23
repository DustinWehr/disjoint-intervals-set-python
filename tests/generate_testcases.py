# from disjointintervals.DisjointIntervalsParametric import DisjointIntervalsParametric
# from disjointintervals.DisjointIntervalsFast import DisjointIntervalsFast
from disjointintervals.disjointintervals_slow4spec import DisjointIntervalsSlowSpec
from .context import disjointintervals
from .types_for_tests import *
from .generate_op_sequences import add_opseqs, del_opseqs
from .helpers_for_tests import run_ops


def run_opseq(opseq: RangeOpSeq) -> List[Interval]:
    # dranges = DisjointIntervalsFast()
    # dranges = DisjointIntervalsParametric()
    dranges = DisjointIntervalsSlowSpec()
    run_ops(dranges, opseq)
    return dranges.intervals()


add_cases: List[KTestCase] = [KTestCase(opseq, run_opseq(opseq)) for opseq in add_opseqs]
del_cases: List[KTestCase] = [KTestCase(opseq, run_opseq(opseq)) for opseq in del_opseqs]

print(f"{len(add_cases) + len(del_cases)} GENERATED CASES")


def test_pytest_showme_the_cases():
    """
    "test" prefix on this fn name causes pytest to run it.    
    """
    print("Add cases")
    for case in add_cases:
        print(case)

    print("\nDelete cases")
    for case in del_cases:
        print(case)

    # causes pytest to show output.
    assert False
