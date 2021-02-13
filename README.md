# About

Four Python 3 implementations of a data structure that efficiently maintains a set of disjoint integer intervals.

Intervals are closed on the left, open on the right. So `[1,2)` means the set `{1}`.

Adjacent intervals are joined, meaning if you add `[1,3)` and `[3,5)` to an empty 
DisjointIntervalsSet, you'll get the single interval set `{[1,5)}`.

These are the main operations:

- `intervals.add(x,y)` - adds `[x,y)` to the set.
- `intervals.delete(x,y)` - deletes `[x,y)` from the set. For example, if `intervals` is the single
interval set `{[1,5)}`, then `intervals.delete(3,4)` will result in `{[1,3),[4,5)}`
- `intervals.get_intersecting(x,y)` - return a list of all the intervals in the set that intersect
`[x,y)`.


## Note to any seekers of jobs at K*****

This repo grew out of my solution to a coding challenge I did while interviewing for a job at K*****. If you found this while looking for a python library to help solve a coding challenge at a company named K*****, I propose telling them you found this, considering:
- Best case scenario: You get honesty points and an opportunity to show off your dev skills by improving an already-good open source repo.
- Worst case scenario: You get honesty points and a different coding challenge. 

## Todo

Cython implementation.


# Testing Correctness

There is code in `tests` for generating and verifying a large number of small tests. 
*The verification is independent of the code in package `disjointintervals`*. For a parameter `m`,
those tests are intended to cover "all the ways" of: 
- adding an interval to 1, 2, ..., or `m` starting disjoint intervals.
- deleting an interval from 1, 2, ..., or `m` starting disjoint intervals.

`m` is set to 3 in the code. You can change it by modifying `tests/opseq_generator.py`.
Currently the set of starting interval-sets should be: 
```
[-1, 1)
[-3, -1), [1, 3)
[-5, -3), [-1, 1), [3, 5)
# And, same as two previous lines, but make intervals as close as possible without getting joined:
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
$ pytest-3 <repo root dir>/tests/generate_testcases.py
```

To run all the currently-enabled tests, without verifying the generated cases, run from `<repo root dir>`,
or `<repo root dir>/tests`:

```
$ pytest-3
```

## Verifying Generated Test Cases

The implementation `disjointintervals_slow4spec.py` was written to be obviously correct, without
any regard to efficiency. It is used to generate, but not to verify, the generated test cases.

Instead, verification is done in `independently_verify_generated_cases.py` using just Python's 
`range` and `set`, by actually generating the integer sets. You can run the verification with 
```
$ pytest-3 <repo root dir>/tests/independently_verify_generated_cases.py
```


## Misc Tests 

- `test_absolute_examples.py` is an untidy set of explicit small test cases that are not intended to
provide full coverage. Rather, I would distill and add a small case whenever I found an error using:
- `test_equivalence.py`, which has code that checks that the 4 different implementations of 
`DisjointIntervalsInterface` produce exactly the same results when run on random sequence of operations. 
I've only left a couple tests enabled in `test_equivalence.py`.


# Performance

I had to get up to interval lists of size close 500k for the `blist` based implementation with its
worst-case `O(log n)`-time ops to beat the `list` and `array` based implementations, with their 
worst-case `O(n)`-time operations. This is because `blist` has much slower get and set ops 
(`O(log n)` machine ops with a significant constant) than python's dynamic arrays do (one to a few 
machine ops). 

`array`-based implementation is 15% - 20% faster than `list`-based, but will currently only work 
with interval endpoints in the range `[0, 2^32 - 1]`. 


## Testing Performance

In order to check performance with assertions turned off:
```
$ python3 - O <repo root dir>/tests/compare_performance.py
```
or 
```
$ pypy3 -O <repo root dir>/tests/compare_performance.py
```


## Asymptotic Complexity of `blist` Implementation 

`add`, and `delete` are all asymptotically optimal in time complexity, in addition to being pretty 
fast in practice; both properties are largely thanks to the excellent `blist` package. 
`get_intersecting` is optimal and fast in practice when the number of returned intervals is not 
large; details below. 

`n` is the number of disjoint intervals.

- `add`: `O(log n)`
- `del`: `O(log n)`
- `get_intersecting`: `O(k + log n)` where `k` is the number of returned intervals. If the 
implementation was changed so that the intervals were returned as a `blist` rather than a 
`List[Interval]`, it's probably possible to do this in time `O(log n)`, due to `blist`'s 
copy-on-write implementation. 
