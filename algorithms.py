from copy import deepcopy

import rationals


def del_extra_zeros(a):
    """
    Deleting extra zeros from the end of list
    """
    b = deepcopy(a)
    while b and b[-1] == 0:
        del b[-1]
    return b


def gcd(a, b):
    """Euclidean algorithm -- return the greatest common divisor of a and b.
    The correctness of the algorithm is guaranteed iff a and b are elements
    of some Euclidean domain. For a and b must be implemented:
    __ne__ to zero, __imod__ each other.
    """
    while b != 0:
        a %= b
        a, b = b, a
    return a


def get_largest_abelian_group(cls1, cls2, exc):
    """Return the largest class of cls1 and cls2, i.e., the class, to which
    both abelian groups can be cast. If both cannot be cast to each other,
    raise exc.
    """
    try:
        cls1(cls2(0))
        return cls1
    except (ValueError, TypeError):
        try:
            cls2(cls1(0))
            return cls2
        except (ValueError, TypeError):
            raise exc


def add_lists(ls1: list, ls2: list):
    """Return the element-wise sum of two lists. If lengths are different,
    the shorter list is completed with zeroes.
    """
    # Make sure ls1 is the shortest.
    if len(ls1) > len(ls2):
        ls1, ls2 = ls2, ls1
    res = [ls1[i] + ls2[i] for i in range(len(ls1))]
    res.extend(deepcopy(ls2[len(ls1):len(ls2)]))
    return res


def sub_lists(ls1: list, ls2: list):
    """Return the element-wise subtraction of two lists."""
    return add_lists(ls1, [-i for i in ls2])


def mul_lists(ls1: list, ls2: list):
    res = [0 for _ in range(len(ls1) + len(ls2))]
    for i in range(len(ls1)):
        for j in range(len(ls2)):
            res[i + j] += ls1[i] * ls2[j]
    return res
