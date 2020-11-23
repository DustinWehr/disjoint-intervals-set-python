from .context import disjointintervals
from .generate_op_sequences import add_opseqs, del_opseqs
from .generate_testcases import add_cases, del_cases

collect_ignore = ["compare_performance.py"]

def pytest_generate_tests(metafunc):
    if "opseq" in metafunc.fixturenames:
        metafunc.parametrize("opseq", add_opseqs + del_opseqs)

    if "testcase" in metafunc.fixturenames:
        metafunc.parametrize("testcase", add_cases + del_cases)