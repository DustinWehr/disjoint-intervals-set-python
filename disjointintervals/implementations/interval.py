from typing import List, Tuple

from DisjointIntervalsSet.disjointintervals.types.disjointintervals import Interval

# NOTE: THERE ARE MANY INEFFICIENT FUNCTIONS IN HERE.
# BUT THEY ARE ONLY USED IN SPECIFICATION CODE AND ASSERTIONS.


def nonempty(r: Interval) -> bool:
    return r[0] < r[1]


def empty(r: Interval) -> bool:
    return r[0] == r[1]


def difference(source: Interval, toremove: Interval) -> List[Interval]:
    """Post: Union of results is a subset of r1

    >>> difference((1,6),(4,10)) 
    [(1, 4)]
    >>> difference((1,6),(-1,10)) 
    []
    >>> difference((1,6),(-3,-1)) 
    [(1, 6)]
    """
    if not intersection_nonempty(source, toremove):
        return [source]

    if source[0] < toremove[0]:
        # assert source[1] > toremove[0] # since we already checked that they intersect
        if source[1] <= toremove[1]:
            return [(source[0], toremove[0])]
        else:  # toremove[1] < source[1]
            return [(source[0], toremove[0]), (toremove[1], source[1])]
    else:  # toremove[0] <= source[0]
        if source[1] <= toremove[1]:
            return []
        else:  # toremove[1] < source[1]
            return [(toremove[1], source[1])]


def subset(r1: Interval, r2: Interval) -> bool:
    return r1[0] >= r2[0] and r1[1] <= r2[1]


def union(r1: Interval, r2: Interval) -> Interval:
    """
    Pre: not separated(r1,r2)
    (so that the union is a single interval.)
    """
    assert not separated(r1, r2)
    r1, r2 = total_sorted(r1, r2)
    return (r1[0], max(r1[1], r2[1]))


def sorted_by_lower_bound(r1: Interval,
                          r2: Interval) -> Tuple[Interval, Interval]:
    return (r1, r2) if r1[0] <= r2[0] else (r2, r1)


def total_sorted(r1: Interval, r2: Interval) -> Tuple[Interval, Interval]:
    if r1[0] < r2[0]:
        return r1, r2
    elif r1[0] > r2[0]:
        return r2, r1
    elif r1[1] <= r2[1]:
        return r1, r2
    else:
        return r2, r1


def separated(r1: Interval, r2: Interval) -> bool:
    """
    r1 = [x1,y1) and r2 = [x2,y2) are separated iff their union is not a single interval
    Equivalently, they are separated iff their intersection is empty and they aren't adjacent (y1 = x2 or y2 = x1).
    Pre: r1 and r2 are nonempty intervals
    """
    assert nonempty(r1) and nonempty(r2), (r1, r2)

    # rename so that r1 <= r2 by lower bound (left endpoint) order
    if r1[0] > r2[0]:
        r1, r2 = r2, r1
    elif r1[0] == r2[0]:
        # then they both contain the number r1[0]
        return False

    # following condition is false exactly when r1 and r2 either overlap or are adjacent
    return r1[1] < r2[0]


def intersection_nonempty(r1: Interval, r2: Interval) -> bool:
    """
    >>> intersection_nonempty((1,6),(4,10))
    True
    >>> intersection_nonempty((4,10),(1,6))
    True
    >>> intersection_nonempty((4,5),(5,7))
    False
    >>> intersection_nonempty((1,3),(4,6))
    False
    >>> intersection_nonempty((4,6),(5,6))
    True
    """
    if empty(r1) or empty(r2):
        return False
    if r1[0] == r2[0]:
        return True
    elif r1[0] < r2[0]:
        return r1[1] > r2[0]
    else:
        return r2[1] > r1[0]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
