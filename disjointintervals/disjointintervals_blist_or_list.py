from typing import Optional, cast, Type
from bisect import bisect_right, bisect_left
# from blist import blist

from disjointintervals.interval import *
from disjointintervals.types.disjointintervals import DisjointIntervalsInterface
from disjointintervals.types.disjointintervals import Interval


class DisjointIntervalsFast(DisjointIntervalsInterface):

    def __init__(self, intervals: List[Interval] = None,
                       list_class: Type[List[Interval]] = list) -> None:
        DisjointIntervalsInterface.__init__(self, intervals)
        self._list_class = list_class
        self._inter = list_class(cast(List[Interval], intervals if intervals else []))  # type:ignore
        self._inter.sort(key=lambda x: x[0])

    def __len__(self) -> int:
        return len(self._inter)

    def _bisect_left(self, x: int):
        return bisect_left(self._inter, (x,x))

    def _bisect_right(self, x: int):
        return bisect_right(self._inter, (x,x))

    def intervals(self) -> List[Interval]:
        return self._inter

    def _index_of_interval_touching_strictly_from_left(self, x: int) -> Optional[int]:
        """
        If there is a range that starts strictly before x, and either contains x or has x
        as its right open endpoint, then return the index of that range. Otherwise return None.
        """
        # With the default lexicographic ordering on tuples, the x - 1 ensures we'll get the index
        # of an existing range starting at x if there is one, rather the index after it.
        ibl_x = bisect_left(self._inter, (x, x - 1))
        if ibl_x > 0:
            assert self._inter[ibl_x - 1][0] < x
            if self._inter[ibl_x - 1][1] >= x:  # its right, open endpoint touches x
                return ibl_x - 1
        return None

    def _add_normalized_old(self, s: int, e: int) -> None:
        """
        Does the same as add, but with stronger preconditions.
        "range set" = the union of the ranges
        Pre:
        - s is in the range set iff it's a left endpoint of some existing range.
        - There is no existing range that starts in [s,e] that ends at or after e (i.e. whose
          right endpoint is greater than e).
        """
        # "ibl_s" for index of bisect_left on s
        ibl_s = self._bisect_left(s)
        ibl_e = self._bisect_left(e)

        if ibl_s == len(self._inter):
            # no intersection
            self._inter.append((s,e))
            return

        # ibl_s < len(self._inter)
        s2, e2 = self._inter[ibl_s]
        if s == s2:
            # Case: [s,e') is a range for some e'. This can only happen at ibl_s.
            if e == e2:
                return  # [s,e) is already a range. Nothing to do.
            # e2 < e
            # We right-extend [s,e2) to [s,e) and then delete any ranges within [s,e)
            self._inter[ibl_s] = (s,e)
            if ibl_s + 1 < ibl_e:
                del self._inter[ibl_s + 1: ibl_e]
            return

        # Case: [s,e') is not a range for any e'.
        # Remains to check if [s',e) is a range for some s' > s
        # [s3,e3) is the range that ends just before or at e
        s3, e3 = self._inter[ibl_e - 1]
        if e3 == e:
            # Case: [s3,e) is a range, where s3 > s. This can only happen at index ibl_e - 1.
            # We left-extend [s2,e) to [s,e) and then delete any ranges strictly within [s,e).
            self._inter[ibl_e - 1] = (s,e)
            del self._inter[ibl_s: ibl_e - 1]
            return

        # Case: Any ranges that lie within [s,e) have neither s nor e as endpoints.
        # We replace all of them with [s,e), keeping the ranges to the left and right of [s,e).
        self._inter = self._inter[:ibl_s] + self._list_class([(s,e)]) + self._inter[ibl_e:]

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
        # "ibl_s" for index of bisect_left on s
        ibl_s = s_index
        # ibl_s = self._bisect_left(s)

        if ibl_s == len(self._inter):
            # no intersection
            self._inter.append((s,e))
            return

        # ibl_s < len(self._inter)
        s2, e2 = self._inter[ibl_s]
        if s == s2:
            # Case: [s,e') is a range for some e'. This can only happen at ibl_s.
            if e == e2:
                return  # [s,e) is already a range. Nothing to do.
            # e2 < e
            # ibl_e = self._bisect_left(e)
            ibl_e = e_index
            # We right-extend [s,e2) to [s,e) and then delete any ranges within [s,e)
            self._inter[ibl_s] = (s,e)
            if ibl_s + 1 < ibl_e:
                del self._inter[ibl_s + 1: ibl_e]
            return
        else:
            # ibl_e = self._bisect_left(e)
            ibl_e = e_index

        # Case: [s,e') is not a range for any e'.
        # Remains to check if [s',e) is a range for some s' > s
        # [s3,e3) is the range that ends just before or at e
        s3, e3 = self._inter[ibl_e - 1]
        if e3 == e:
            # Case: [s3,e) is a range, where s3 > s. This can only happen at index ibl_e - 1.
            # We left-extend [s2,e) to [s,e) and then delete any ranges strictly within [s,e).
            self._inter[ibl_e - 1] = (s,e)
            del self._inter[ibl_s: ibl_e - 1]
            return

        # Case: Any ranges that lie within [s,e) have neither s nor e as endpoints.
        # We replace all of them with [s,e), keeping the ranges to the left and right of [s,e).
        self._inter = self._inter[:ibl_s] + self._list_class([(s,e)]) + self._inter[ibl_e:]


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
            s2, e2 = self._inter[ibl_s - 1]
            if e2 >= s:
                # There's a range [s2,e2), which starts to the left of s, that either touches
                # or overlaps [s,e). So, it's equivalent to call self.add(s2,e). Thus redefine s:
                s = s2
                new_s_index = ibl_s - 1

        ibl_e = self._bisect_left(e)
        new_e_index = ibl_e
        e_updated = False
        if ibl_e < len(self._inter):
            s2, e2 = self._inter[ibl_e]
            # There's a range that starts at or after e.
            assert e <= s2
            if e == s2:
                # [e,e2) is an existing range, which means this call to add should effectively
                # union [s,e) and [e,e2). So it's equivalent to call self.add(s,e2), so redefine e:
                e = e2
                # UNSURE!!!!!!!!!!!!
                new_e_index = ibl_e + 1
                e_updated = True

        if not e_updated and ibl_e > 0:
            s2, e2 = self._inter[ibl_e - 1]
            if e2 > e:
                # [s2,e2) is a range that starts to the left of e, and finishes strictly after e, which means this call
                # to add should effectively union [s,e) and [s2,e2).
                # So it's equivalent to call self.add(s,e2), so redefine e:
                e = e2
                # UNSURE
                # new_e_index is still ibl_e

        self._add_normalized(s, e, new_s_index, new_e_index)

    def _add_old(self, s: int, e: int) -> None:
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
        ibl_e = self._bisect_left(e)

        if ibl_s > 0:
            # There's a range [s2,e2) that starts to the left of s.
            s2, e2 = self._inter[ibl_s - 1]
            if e2 >= s:
                # There's a range [s2,e2), which starts to the left of s, that either touches
                # or overlaps [s,e). So, it's equivalent to call self.add(s2,e). Thus redefine s:
                s = s2

        if ibl_e < len(self._inter):
            s2, e2 = self._inter[ibl_e]
            # There's a range that starts at or after e.
            assert e <= s2
            if e == s2:
                # [e,e2) is an existing range.
                # So it's equivalent to call self.add(s,e2), so redefine e:
                e = max(e, e2)

        if ibl_e > 0:
            s2, e2 = self._inter[ibl_e - 1]
            if e2 > e:
                # There's a range that starts to the left of e, and finishes strictly after e.
                # So it's equivalent to call self.add(s,e2), so redefine e:
                e = e2

        self._add_normalized(s, e)

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

        # We want j to be the index of a range starting at or before s, if there is one.
        # The next if/elif blocks accomplish that.
        j = self._bisect_left(s)
        if j == len(self._inter):
            # no existing range starts with s, and moreover
            # there is a range that starts strictly before s
            j -= 1
        elif self._inter[j][0] > s:
            # no existing range starts with s.
            if j > 0:
                j -= 1
            else:
                # There is no range that starts before s either.
                j = None

        if j is not None:
            s1, e1 = self._inter[j]
            if s1 <= s and e <= e1:
                # PART 1
                # The cases where [s,e) is a subset of an existing range.

                if s1 < s:
                    if e < e1:
                        # s1 < s < e < e1
                        # [s1,e1) strictly contains [s,e) on both sides, so [s1,e1) gets split in two,
                        # into [s1,s) and [e,e1)
                        self._inter[j] = (s1, s)
                        self._inter.insert(j + 1, (e, e1))
                    else:  # e == e1. one truncation suffices
                        self._inter[j] = (s1, s)
                else:  # s1 == s
                    if e < e1:
                        self._inter[j] = (e, e1)
                    else:  # e == e1. [s,e) is an existing range
                        del self._inter[j]

                return

        # PART 2
        # These are exactly the cases where [s,e) is NOT a subset of an existing range.
        # assert all(not subset((s,e),r) for r in self.intervals())
        i = self._index_of_interval_touching_strictly_from_left(s)
        if i is not None:
            s1, e1 = self._inter[i]
            assert s <= e1
            # truncate [s1,e1)
            self._inter[i] = (s1, s)

        i = self._index_of_interval_touching_strictly_from_left(e)
        if i is not None:
            s1, e1 = self._inter[i]
            assert s < s1  # otherwise we would have been in the PART 1 cases
            assert s1 < e
            if e < e1:
                # truncate [s1,e1)
                self._inter[i] = (e, e1)
            else:  # e == e1
                # [s1,e1) needs to be deleted and not replaced with anything, which will happen
                # shortly outside this conditional.
                pass

        # just remains to delete all the ranges within [s,e).
        ibl_s = self._bisect_left(s)
        ibl_e = self._bisect_left(e)
        del self._inter[ibl_s: ibl_e]

    def get_intersecting(self, s: int, e: int) -> List[Interval]:
        """
        Return the list of all intervals in self that intersect [s,e). The individual intervals are not modifed.
        """
        se = (s, e)
        ibl_s = self._bisect_left(s)
        ibr_e = self._bisect_right(e)
        rv = []

        start = max(ibl_s - 1, 0)
        end = min(ibr_e + 1, len(self._inter))

        if self._list_class == list:
            for i in range(start, end):
                r = self._inter[i]
                if intersection_nonempty(se, r):
                    rv.append(r)
        else:
            # This version is more efficient for self._inter of type blist, but for self._inter of type list it might
            # unnecessarily create a new array.
            for r in self._inter[start:end]:
                if intersection_nonempty(se, r):
                    rv.append(r)

        return rv
