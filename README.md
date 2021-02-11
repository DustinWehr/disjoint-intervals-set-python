# Todo


## Done

- tried. only helped very slightly, and I think had some drawbacks. USE MUTABLE STRUCTS FOR INTERVALS - 
- pass. Optimal `get_intersecting`
- pass. Try using as part of list data structure that supports efficient insert/delete ops.
- done. Mypy
- done. Remove sortedlist implementation?
- Look into CPython's `bisect` for `blist`; didn't look at the C code.
See commit 21ba8e56 for approach taken.
- Rename `DisjointIntervalsFast`, make it an ABC, and give list and blist implementations their own classes.


# Note to any seekers of jobs at K*****

This repo grew out of my solution to a coding challenge I did while interviewing for a job at K*****. If you are looking
for a python library to help solve a coding challenge at a company named K*****, I propose telling them you found this, 
considering:
- Best case scenario: you get honesty points and an opportunity to show off your dev skills by improving an already-good 
open source repo.
- Worst case scenario: you get honesty points and a different coding challenge. 

# Performance

## Why `blist`-based implementation is worse than `list`-based

I think it is just because blist's get and set are significantly slower.

**NO the following explanation appears wrong, based on 9 Feb 2021 tests**:

The apparent advantage of `blist` over `list` disappeared when I changed:
```
self._inter = self._inter[:ibl_s] + self._ListOrBList([(s,e)]) + self._inter[ibl_e:]
```
to
```
self._inter[ibl_s:ibl_e] = self._ListOrBList([(s, e)])
``` 

## Complexity

`add`, and `delete` are all asymptotically optimal in time complexity, in addition to being fast in practice; both 
properties are largely thanks to the excellent `blist` package. `get_intersecting` is optimal and fast in practice
when the number of returned intervals is not large; details below. 

`n` is the number of disjoint intervals.

- `add`: `O(log n)`
- `del`: `O(log n)`
- `get_intersecting`: `O(k + log n)` where `k` is the number of returned intervals. If the intervals are returned as
a `blist` (typed as `Iterable[Interval]`) rather than a `List[Interval]`, it's probably possible to do this in time 
`O(log n)`, due to `blist`'s copy-on-write implementation. This is a TODO. 


## Testing Performance

In order to check performance with assertions turned off:
```
tests$ python3 - O compare_performance.py
```
or 
```
$ pypy3 - O compare_performance.py
```


# Testing Correctness

There is code in `tests` for generating and, independently of the code in package `disjointintervals`, 
verifying a large number of small tests, specifically for "all the ways" of: 
- adding an interval to 1,2 or 3 disjoint intervals.
- deleting an interval from 1,2 or 3 disjoint intervals.

You can increase the number of starting intervals in `tests/opseq_generator.py`. Currently they 
should be: 
```
[-1, 1)
[-3, -1), [1, 3)
[-5, -3), [-1, 1), [3, 5)
# same as two previous lines, but make intervals as close as possible without getting joined.
[-4, -1), [0, 3)  
[-5, -3), [-2, 1), [2, 5)
```
For example, "all the ways" for `(-1, 1)` means adding or deleting one of:
```
[-3,-2), [-2,-1), [-1, 0), [0,1), [1,2), [2, 3)
```
And "all the ways" for `[-3, -1), [1, 3)` means adding or deleting one of:
```
[-5,-4), [-5,-3), ..., [-5, 5), [-4, -3), [-4, -2), ..., [3, 4), [3, 5), [4, 5)
```
You can see the generated test cases by doing 
```
tests$ pytest case_generator.py
```

To run all the currently-enabled tests, without verifying the generated cases:

```
tests$ pytest
```

## Verifying Generated Test Cases

The implementation `disjointintervals_slow4spec.py` was written to be obviously correct, without
any regard to efficiency. It is used to generate, but not to verify, the generated test cases.
Verification is done in `independently_verify_generated_cases.py` using just Python's `range` and `set`, by 
actually generating the integer sets. You can run the verification with 
```
tests$ pytest independently_verify_generated_cases.py
```


## Misc Tests 

- `test_absolute_examples.py` is an untidy set of explicit small test cases that are not intended to
provide full coverage. Rather, I would distill and add a small case whenever I found an error using:
- `test_equivalence.py`, which has code that checks that different implementations of 
`DisjointIntervalsInterface` produce exactly the same results when run on random sequence of operations. 
I've only left a couple tests enabled in `test_equivalence.py`.

