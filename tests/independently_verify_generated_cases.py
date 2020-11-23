# python verify_generated_cases

from typing import List, Iterable, NamedTuple, Set

# types and the test case lists should be the only dependencies
from .types_for_tests import *
from .generate_testcases import add_cases, del_cases

def interval_set_to_element_set(ranges: Iterable[Interval]) -> Set[int]:
    return set(x for raange in (range(left,right) for (left,right) in ranges) for x in raange)
    
def verify_add_case(case: KTestCase):
    assert case.opseq[-1][0] == 'a'
    ranges_to_add = (op[1] for op in case.opseq)
    # print(ranges_to_add)
    computed_as_set = interval_set_to_element_set(ranges_to_add)
    expected_as_set = interval_set_to_element_set(case.expected) 
    assert computed_as_set == expected_as_set

def verify_del_case(case: KTestCase):
    assert case.opseq[-1][0] == 'd'

    ranges = [op[1] for op in case.opseq]
    
    computed_as_set = interval_set_to_element_set(ranges[:-1])
    computed_as_set.difference_update(interval_set_to_element_set([ranges[-1]])) 

    expected_as_set = interval_set_to_element_set(case.expected) 
    assert computed_as_set == expected_as_set
    
def test_verify_add_cases(testcase):
    for case in add_cases:
        verify_add_case(case)

def test_verify_del_cases(testcase):
    for case in del_cases:
        verify_del_case(case)