from typing import Type, Iterable, List, Union, Any
from bisect import bisect_right, bisect_left
# from DisjointIntervalsSet.disjointintervals.implementations.listlike_backed.bisect_no_cpython import bisect_right_py, bisect_left_py

from DisjointIntervalsSet.disjointintervals.implementations.interval_util import subset, intersection_nonempty
from DisjointIntervalsSet.disjointintervals.types.disjointintervals import DisjointIntervalsInterface, TupInterval

# from DisjointIntervalsSet.disjointintervals.types.disjointintervals import Interval

# this is needed in order to allow DisjointIntervalsArray to redefine it
Interval = Any

# ABC = Abstract Base Class
class DisjointIntervalsListlikeABC(DisjointIntervalsInterface):

    def __init__(self, intervals: Iterable[Interval] = None):
        DisjointIntervalsInterface.__init__(self)
        self._inter = self._listlist_constructor(intervals if intervals else [])
        self._sort()

    def _listlike_contstructor(self, itemsiter) -> Any:
        return list(itemsiter)

    def __len__(self) -> int:
        return len(self._inter)

    """
    The following 7 functions are only here so that they can be overwritten by the DisjointIntervalsArray subclass.
    :-(
    """
    def _sort(self) -> None:
        self._inter.sort(key=lambda x: self._interval_to_left_endpoint(x))
    def _interval(self, left: int, right :int) -> Interval:
        return left, right
    def _interval_to_left_endpoint(self, interval: Interval) -> int:
        return interval[0]
    def _get_left_endpoint(self, i: int) -> int:
        return self._inter[i][0]
    def _get_right_endpoint(self, i: int) -> int:
        return self._inter[i][1]
    def _get_unpack_interval(self, i: int) -> Interval:
        return self._inter[i]
    def _intersection_nonempty(self, r1, r2) -> bool:
        return intersection_nonempty(r1, r2)


    def _replace_slice(self, start, stop_exclusive, newelem):
        self._inter[start:stop_exclusive] = self._listlist_constructor([newelem])

    def _bisect_left(self, x: int) -> int:
        return bisect_left(self._inter, self._interval(x, x))
        # return bisect_left_py(self._inter, x)

    # makes list implementation worse. too much overhead.
    # def _bisect_left(self, x: int, left_bound_start=0, right_bound_start=None):
    #     return bisect_left(self._inter, self._interval(x, x), left_bound_start, right_bound_start or len(self))

    # even this makes both implementations slower:
    # def _bisect_left(self, x: int, left_bound_start=0):
    #     return bisect_left(self._inter, self._interval(x, x), left_bound_start)

    def _bisect_right(self, x: int) -> int:
        return bisect_right(self._inter, self._interval(x, x))
        # return bisect_right_py(self._inter, x)

    def intervals(self) -> List[TupInterval]:
        return self._inter

    def _index_of_interval_touching_strictly_from_left(self, x: int, ibl_x=None) -> int:
        """
        If there is a range that starts strictly before x, and either contains x or has x
        as its right open endpoint, then return the index of that range.
        Otherwise return -1.
        """
        # With the default lexicographic ordering on tuples, the x - 1 ensures we'll get the index
        # of an existing range starting at x if there is one, rather the index after it.
        if ibl_x is None:
            ibl_x = self._bisect_left(x)
        if ibl_x > 0:
            assert self._get_left_endpoint(ibl_x - 1) < x
            if self._get_right_endpoint(ibl_x - 1) >= x:  # its right, open endpoint touches x
                return ibl_x - 1
        return -1

    def _add_normalized(self, s: int, e: int, s_index: int, e_index: int) -> None:
        """
        Does the same as add, but with stronger preconditions.
        "range set" = the union of the ranges
        Pre:
        - No range has open endpoint s.
        - s is in the range set iff it's a left endpoint of some existing range.
        - There is no existing range that starts in [s,e] that ends at or after e (i.e. whose
          right endpoint is greater than e).
        """
        assert e_index == self._bisect_left(e)
        assert s_index == self._bisect_left(s)

        # "ibl_s" for *i*ndex of *b*isect_*l*eft on s
        ibl_s = s_index
        
        if ibl_s == len(self._inter):
            # no intersection
            self._inter.append(self._interval(s, e))
            return

        # ibl_s < len(self._inter)
        s2, e2 = self._get_unpack_interval(ibl_s)
        if s == s2:
            # Case: [s,e') is a range for some e'. This can only happen at ibl_s.
            if e == e2:
                return  # [s,e) is already a range. Nothing to do.
            # e2 < e
            ibl_e = e_index
            # We right-extend [s,e2) to [s,e) and then delete any ranges within [s,e)
            self._inter[ibl_s] = self._interval(s, e)
            if ibl_s + 1 < ibl_e:
                del self._inter[ibl_s + 1: ibl_e]
            return
        else:
            # ibl_e = self._bisect_left(e)
            ibl_e = e_index

        # Case: [s,e') is not a range for any e'.
        # Remains to check if [s',e) is a range for some s' > s
        # [s3,e3) is the range that ends just before or at e
        s3, e3 = self._get_unpack_interval(ibl_e - 1)
        if e3 == e:
            # Case: [s3,e) is a range, where s3 > s. This can only happen at index ibl_e - 1.
            # We left-extend [s2,e) to [s,e) and then delete any ranges strictly within [s,e).
            self._inter[ibl_e - 1] = self._interval(s, e)
            del self._inter[ibl_s: ibl_e - 1]
            return

        # Case: Any ranges that lie within [s,e) have neither s nor e as endpoints.
        # We replace all of them with [s,e), keeping the ranges to the left and right of [s,e).
        self._replace_slice(ibl_s, ibl_e, self._interval(s,  e))

    def add(self, s: int, e: int) -> None:
        """
        Approach is to find the smallest s' and largest e' such that [s',e') contains [s,e)
        and add(s',e') is equivalent to add(s,e). Then:
        - s' is either s or the left endpoint of an existing range.
        - e' is either e or the right endpoint of an existing range.
        That allows us to use _add_normalized.
        """
        if s >= e:
            return  # empty range

        ibl_s = self._bisect_left(s)
        new_s_index = ibl_s
        if ibl_s > 0:
            # There's a range [s2,e2) that starts to the left of s.
            s2, e2 = self._get_unpack_interval(ibl_s - 1)
            if e2 >= s:
                # There's a range [s2,e2), which starts to the left of s, that either touches
                # or overlaps [s,e). So, it's equivalent to call self.add(s2,e). Thus redefine s:
                s = s2
                new_s_index = ibl_s - 1

        ibl_e = self._bisect_left(e)
        # correct I think, but the extra arithmetic and len call makes list implementation worse:
        # ibl_e = self._bisect_left(e, ibl_s, min(len(self), ibl_s + (e-s)))
        # even this makes both implementations slower:
        # ibl_e = self._bisect_left(e, ibl_s)
        new_e_index = ibl_e
        e_updated = False
        if ibl_e < len(self._inter):
            s2, e2 = self._get_unpack_interval(ibl_e)
            # There's a range that starts at or after e.
            assert e <= s2
            if e == s2:
                # [e,e2) is an existing range, which means this call to add should effectively
                # union [s,e) and [e,e2). So it's equivalent to call self.add(s,e2), so redefine e:
                e = e2
                new_e_index = ibl_e + 1  # TODO: explain
                e_updated = True

        if not e_updated and ibl_e > 0:
            s2, e2 = self._get_unpack_interval(ibl_e - 1)
            if e2 > e:
                # [s2,e2) is a range that starts to the left of e, and finishes strictly after e, which means this call
                # to add should effectively union [s,e) and [s2,e2).
                # So it's equivalent to call self.add(s,e2), so redefine e:
                e = e2
                # new_e_index is still ibl_e # TODO: explain

        self._add_normalized(s, e, new_s_index, new_e_index)

    def delete(self, s: int, e: int) -> None:
        """
        Modify the intervals in self so that intset(self) does not contain any number in intset([s,e)).
        """
        if s >= e:
            # [s,e) is empty. perhaps would be wise to make this violate a precondition.
            return
        if len(self._inter) == 0:
            return  # no ranges in data structure

        # The remaining cases are divided into PART 1 and PART 2.
        # See comments below.

        ibl_s = self._bisect_left(s)
        # We want j to be the index of a range starting at or before s, if there is one.
        # The next if/elif blocks accomplish that.
        j = ibl_s
        if j == len(self._inter):
            # no existing range starts with s, and moreover
            # there is a range that starts strictly before s
            j -= 1
        elif self._get_left_endpoint(j) > s:
            # no existing range starts with s.
            if j > 0:
                j -= 1
            else:
                # There is no range that starts before s either.
                j = -1

        if j != -1:
            s1, e1 = self._get_unpack_interval(j)
            if s1 <= s and e <= e1:
                # PART 1
                # The cases where [s,e) is a subset of an existing range.

                if s1 < s:
                    if e < e1:
                        # s1 < s < e < e1
                        # [s1,e1) strictly contains [s,e) on both sides, so [s1,e1) gets split in two,
                        # into [s1,s) and [e,e1)
                        self._inter[j] = self._interval(s1,  s)
                        self._inter.insert(j + 1, self._interval(e,  e1))
                    else:  # e == e1. one truncation suffices
                        self._inter[j] = self._interval(s1,  s)
                else:  # s1 == s
                    if e < e1:
                        self._inter[j] = self._interval(e,  e1)
                    else:  # e == e1. [s,e) is an existing range
                        del self._inter[j]

                return

        # Note: if we get here, self._inter has not been modified, so ibl_s is still correct.
        assert ibl_s == self._bisect_left(s)

        # PART 2
        # These are exactly the cases where [s,e) is NOT a subset of an existing range.
        # assert all(not subset(self._interval(s,  e), r) for r in self.intervals())
        i = self._index_of_interval_touching_strictly_from_left(s, ibl_s)
        if i != -1:
            s1, e1 = self._get_unpack_interval(i)
            assert s <= e1
            # truncate [s1,e1)
            self._inter[i] = self._interval(s1,  s)
            # ibl_s remains valid.
            assert ibl_s == self._bisect_left(s)

        ibl_e = self._bisect_left(e)
        i = self._index_of_interval_touching_strictly_from_left(e, ibl_e)
        if i != -1:
            s1, e1 = self._get_unpack_interval(i)
            assert s < s1  # otherwise we would have been in the PART 1 cases
            assert s1 < e
            if e < e1:
                # truncate [s1,e1) to [e,e1)
                self._inter[i] = self._interval(e,  e1)
                ibl_e -= 1  # insertion position of e changed.
            else:  # e == e1
                # [s1,e1) needs to be deleted and not replaced with anything, which will happen
                # shortly outside this conditional.
                pass

        assert ibl_s == self._bisect_left(s)
        assert ibl_e == self._bisect_left(e)
        # ibl_s = self._bisect_left(s)
        # ibl_e = self._bisect_left(e)

        # just remains to delete all the ranges within [s,e).
        del self._inter[ibl_s: ibl_e]

    def get_intersecting(self, s: int, e: int) -> List[Interval]:
        """
        Return the list of all intervals in self that intersect [s,e). The individual intervals are not modifed.
        """
        se = self._interval(s,  e)
        ibl_s = self._bisect_left(s)
        ibr_e = self._bisect_right(e)
        rv = []

        start = max(ibl_s - 1, 0)
        end = min(ibr_e + 1, len(self._inter))

        if self._listlist_constructor == list:
            for i in range(start, end):
                r = self._inter[i]
                if self._intersection_nonempty(se, r):
                    rv.append(r)
        else:
            # This version is more efficient for self._inter of type blist, but for self._inter of type list it might
            # unnecessarily create a new array.
            for r in self._inter[start:end]:
                if self._intersection_nonempty(se, r):
                    rv.append(r)

        return rv


