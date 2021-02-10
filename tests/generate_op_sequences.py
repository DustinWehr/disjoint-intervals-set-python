from typing import List
from .types_for_tests import RangeOpSeq

SIZES = range(1, 4)
add_opseqs: List[RangeOpSeq] = []
del_opseqs: List[RangeOpSeq] = []
for size in SIZES:
    # when close == True, makes the initial ranges as close as possible without getting joined
    for close in {False, True}:
        init_ranges_nonneg = [(x - (1 if close else 0), x + 2) for x in range(0, size * 4, 4)]
        init_ranges = [((x - (size * 4 - 2) // 2), (y - (size * 4 - 2) // 2)) for x, y in init_ranges_nonneg]

        endpoints = [x[0] for x in init_ranges] + [x[1] for x in init_ranges]
        test_endpoints = list(range(min(endpoints) - 1, max(endpoints) + 2, 1))
        test_ranges = [(x, y) for x in test_endpoints for y in test_endpoints if x < y]
        # print(test_endpoints, "\n", test_ranges)
        # print()

        case_init = [('a', r) for r in init_ranges]
        add_opseqs.extend((case_init + [('a', r2)] for r2 in test_ranges))
        del_opseqs.extend((case_init + [('d', r2)] for r2 in test_ranges))

# def range2str(r):
#     return f"[{r[0]},{r[1]})"
