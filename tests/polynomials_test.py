import pytest

from algorithms import gcd
from integer_residues import FiveElementsField
from polynomials import Polynomials
from rationals import Rationals

TEST_INIT = [
    ([], FiveElementsField),
    ([1, 2], FiveElementsField),
    ([1, FiveElementsField(2)], FiveElementsField),
    ([], Rationals),
    ([1, 2], Rationals),
    ([1, Rationals(2)], Rationals),
    ([Rationals(1), Rationals(2, 3)], Rationals),
    (Polynomials([], FiveElementsField), None),
    (Polynomials([], Rationals), None),
    ([], int),
    ([1, 2], int),
    ([], float),
    ([1, 2], float),
    ([1, 2.0], float),
]


@pytest.mark.parametrize("arg1,arg2", TEST_INIT)
def test_init(arg1, arg2):
    Polynomials(arg1, arg2)


TEST_BAD_INIT = [
    ([1.0], FiveElementsField),
    ([Rationals(0)], FiveElementsField),
    ([0.0], Rationals),
    ([FiveElementsField(0)], Rationals),
    (1, None),
    (Rationals(0), None),
    ([Rationals(0)], int),
    (FiveElementsField(0), int),
    ([Rationals(0)], int),
    (FiveElementsField(0), int),
    ([], str),
    ([1], str),
    (['s'], int),
]


@pytest.mark.parametrize("arg1,arg2", TEST_BAD_INIT)
def test_bad_init(arg1, arg2):
    with pytest.raises(TypeError):
        Polynomials(arg1, arg2)


TEST_EQ = [
    (Polynomials([0, 0], Rationals), Polynomials([], Rationals)),
    (Polynomials([0, 0], Rationals), 0),
    (Polynomials([0, 0], Rationals), Rationals(0)),
    (Polynomials([1, 0, 0], Rationals), Polynomials([1, 0], Rationals)),
    (Polynomials([1, 0, 0], Rationals), 1),
    (Polynomials([1, 0, 0], Rationals), Rationals(1)),
    (Polynomials([1, 2], int), Polynomials(Polynomials([1, 2, 0, 0], int))),
]


@pytest.mark.parametrize("arg1,arg2", TEST_EQ)
def test_eq(arg1, arg2):
    assert arg1 == arg2


TEST_NOT_EQ = [
    (Polynomials([], Rationals), Polynomials([], FiveElementsField)),
    (Polynomials([1, 2], Rationals), Polynomials([1, 2], FiveElementsField)),
    (Polynomials([1, 2], int), Polynomials([1, 2], FiveElementsField)),
    (Polynomials([1], Rationals), FiveElementsField(1)),
]


@pytest.mark.parametrize("arg1,arg2", TEST_NOT_EQ)
def test_not_eq(arg1, arg2):
    assert arg1 != arg2


TEST_SUM = [
    (
        Polynomials([1, 2], FiveElementsField),
        Polynomials([0, 3], FiveElementsField),
        Polynomials([1], FiveElementsField)
    ),
    (
        Polynomials([1, 2], FiveElementsField),
        Polynomials([0, 3], int),
        Polynomials([1], FiveElementsField)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Polynomials([-1, -2, -3], Rationals),
        Polynomials([], Rationals)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Rationals(-1),
        Polynomials([0, 2, 3], Rationals)
    ),
    (
        Rationals(-1),
        Polynomials([1, 2, 3], Rationals),
        Polynomials([0, 2, 3], Rationals)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Polynomials([-1.0, -2.0, -3.0], float),
        Polynomials([], float)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        float(-1),
        Polynomials([0, 2, 3], float)
    ),
    (
        float(-1),
        Polynomials([1, 2, 3], Rationals),
        Polynomials([0, 2, 3], float)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        int(-1),
        Polynomials([0, 2, 3], Rationals)
    ),
    (
        int(-1),
        Polynomials([1, 2, 3], Rationals),
        Polynomials([0, 2, 3], Rationals)
    ),
]


@pytest.mark.parametrize("x,y,expected", TEST_SUM)
def test_sum(x, y, expected):
    assert x + y == expected


TEST_SUB = [
    (
        Polynomials([1, 2], FiveElementsField),
        Polynomials([0, 3], FiveElementsField),
        Polynomials([1, -1], FiveElementsField)
    ),
    (
        Polynomials([1, 2], FiveElementsField),
        Polynomials([0, 3], int),
        Polynomials([1, -1], FiveElementsField)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Polynomials([-1, -2, -3], Rationals),
        Polynomials([2, 4, 6], Rationals)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Rationals(-1),
        Polynomials([2, 2, 3], Rationals)
    ),
    (
        Rationals(-1),
        Polynomials([1, 2, 3], Rationals),
        -Polynomials([2, 2, 3], Rationals)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Polynomials([-1.0, -2.0, -3.0], float),
        Polynomials([2.0, 4.0, 6.0], float)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        float(-1),
        Polynomials([2, 2, 3], float)
    ),
    (
        float(-1),
        Polynomials([1, 2, 3], Rationals),
        -Polynomials([2, 2, 3], float)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        int(-1),
        Polynomials([2, 2, 3], Rationals)
    ),
    (
        int(-1),
        Polynomials([1, 2, 3], Rationals),
        -Polynomials([2, 2, 3], Rationals)
    ),
]


@pytest.mark.parametrize("x,y,expected", TEST_SUB)
def test_sub(x, y, expected):
    assert x - y == expected


TEST_DEGREE = [
    (Polynomials([0, 0, 0], int), -1),
    (Polynomials([], float), -1),
    (Polynomials([2, 0, 0], Rationals), 0),
    (Polynomials([1, 0, 1], int), 2),
    (Polynomials([1, 0, 1, 0, 1, 0, 0, 0], FiveElementsField), 4),
]


@pytest.mark.parametrize("x,expected", TEST_DEGREE)
def test_degree(x, expected):
    assert x.degree() == expected


TEST_MUL = [
    (
        Polynomials([1, 2], FiveElementsField),
        Polynomials([0, 3], FiveElementsField),
        Polynomials([0, 3, 1], FiveElementsField)
    ),
    (
        Polynomials([1, 2], FiveElementsField),
        Polynomials([0, 3], int),
        Polynomials([0, 3, 1], FiveElementsField)
    ),
    (
        Polynomials([-2, 1], Rationals),
        Polynomials([2, 1], Rationals),
        Polynomials([-4, 0, 1], Rationals)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        Rationals(-1),
        -Polynomials([1, 2, 3], Rationals)
    ),
    (
        Rationals(-1),
        Polynomials([1, 2, 3], Rationals),
        -Polynomials([1, 2, 3], Rationals)
    ),
    (
        Polynomials([1, -1, 1], Rationals),
        Polynomials([1.0, 1.0], float),
        Polynomials([1, 0, 0, 1], float)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        float(-1),
        -Polynomials([1, 2, 3], float)
    ),
    (
        float(-1),
        Polynomials([1, 2, 3], Rationals),
        -Polynomials([1, 2, 3], float)
    ),
    (
        Polynomials([1, 2, 3], Rationals),
        int(-1),
        -Polynomials([1, 2, 3], Rationals)
    ),
    (
        int(-1),
        Polynomials([1, 2, 3], Rationals),
        -Polynomials([1, 2, 3], Rationals)
    ),
]


@pytest.mark.parametrize("x,y,expected", TEST_MUL)
def test_mul(x, y, expected):
    assert x * y == expected


TEST_REPR = [
    (
        Polynomials([1, 2], FiveElementsField),
        "Polynomials([FiveElementsField(1), FiveElementsField(2)], "
        + "FiveElementsField)"
    ),
    (
        Polynomials([0, 0], FiveElementsField),
        "Polynomials([], "
        + "FiveElementsField)"
    ),
    (
        Polynomials([1, Rationals(1, 2)], Rationals),
        "Polynomials([Rationals(1, 1), Rationals(1, 2)], "
        + "Rationals)"
    ),
    (
        Polynomials([1, 2], int),
        "Polynomials([1, 2], "
        + "int)"
    ),
    (
        Polynomials([1, 2], float),
        "Polynomials([1.0, 2.0], "
        + "float)"
    ),
]


@pytest.mark.parametrize("x,expected", TEST_REPR)
def test_repr(x, expected):
    assert repr(x) == expected


TEST_STR = [
    (
        Polynomials([1, 2], FiveElementsField),
        "_2_*X + _1_"
    ),
    (
        Polynomials([], FiveElementsField),
        "_0_"
    ),
    (
        Polynomials([0, 1, 1], Rationals),
        "X^2 + X"
    ),
    (
        Polynomials([3, 0, 1], int),
        "X^2 + 3"
    ),
    (
        Polynomials([2, Rationals(1, 3), 1, 0, Rationals(3, 2)], Rationals),
        "3/2*X^4 + X^2 + 1/3*X + 2"
    ),
]


@pytest.mark.parametrize("x,expected", TEST_STR)
def test_str(x, expected):
    assert str(x) == expected


TEST_SHIFT = [
    (
        Polynomials([1, 2], FiveElementsField),
        2,
        Polynomials([0, 0, 1, 2], FiveElementsField),
    ),
    (
        Polynomials([1, 2], FiveElementsField),
        0,
        Polynomials([1, 2], FiveElementsField),
    ),
    (
        Polynomials([0, 1], Rationals),
        1,
        Polynomials([0, 0, 1], Rationals),
    ),
    (
        Polynomials([], int),
        3,
        Polynomials([], int),
    ),
]


@pytest.mark.parametrize("x,n,expected", TEST_SHIFT)
def test_shift(x, n, expected):
    assert x.shift(n) == expected


def test_bad_shift():
    with pytest.raises(ValueError):
        Polynomials([], int).shift(-4)
        Polynomials([1], int).shift(-1)


TEST_TO_MONIC = [
    (
        Polynomials([1, 2, 0], FiveElementsField),
        Polynomials([3, 1], FiveElementsField),
    ),
    (
        Polynomials([], FiveElementsField),
        Polynomials([], FiveElementsField),
    ),
    (
        Polynomials([0, 1, 1], Rationals),
        Polynomials([0, 1, 1], Rationals),
    ),
    (
        Polynomials([3, Rationals(1, 3), 1, 0, Rationals(3, 2)], Rationals),
        Polynomials([2, Rationals(2, 9), Rationals(2, 3), 0, 1], Rationals),
    ),
]


@pytest.mark.parametrize("x,expected", TEST_TO_MONIC)
def test_to_monic(x, expected):
    assert x.to_monic() == expected


def test_bad_to_monic():
    with pytest.raises(TypeError):
        Polynomials([1, 2], int).to_monic()


TEST_DIVISION = [
    (
        Polynomials([0, -1, 0, 0, 0, 1], Rationals),
        Polynomials([0, 0, 1], Rationals),
        Polynomials([0, 0, 0, 1], Rationals),
        Polynomials([0, -1], Rationals),
    ),
    (
        Polynomials([0, -1, 0, 0, 0, 1], Rationals),
        Polynomials([2, -3, 1], Rationals),
        Polynomials([15, 7, 3, 1], Rationals),
        Polynomials([-30, 30], Rationals),
    ),
    (
        Polynomials([0, -1, 0, 0, 0, 1], FiveElementsField),
        Polynomials([2, -3, 1], FiveElementsField),
        Polynomials([0, 2, 3, 1], FiveElementsField),
        Polynomials([], FiveElementsField),
    ),
    (
        Polynomials([1, 1], Rationals),
        Polynomials([1, 1, 1], Rationals),
        Polynomials([], Rationals),
        Polynomials([1, 1], Rationals),
    ),
    (
        Polynomials([], Rationals),
        Polynomials([1, 1, 1], Rationals),
        Polynomials([], Rationals),
        Polynomials([], Rationals),
    ),
    (
        Polynomials([6, 0, 0, 5, 0, 1], Rationals),
        Polynomials([3, 2, 1], int),
        Polynomials([-6, 6, -2, 1], Rationals),
        Polynomials([24, -6], Rationals),
    ),
    (
        2 * Polynomials([6, 0, 0, 5, 0, 1], Rationals),
        2 * Polynomials([3, 2, 1], Rationals),
        Polynomials([-6, 6, -2, 1], Rationals),
        2 * Polynomials([24, -6], Rationals),
    ),
    (
        Polynomials([6, 0, 0, 5, 0, 1], Rationals),
        2 * Polynomials([3, 2, 1], Rationals),
        Rationals(1, 2) * Polynomials([-6, 6, -2, 1], Rationals),
        Polynomials([24, -6], Rationals),
    ),
    (
        Polynomials([3, -5, 1, 1], int),
        Polynomials([-1, 1], Rationals),
        Polynomials([-3, 2, 1], Rationals),
        Polynomials([], Rationals),
    ),
]


@pytest.mark.parametrize("x,y,q,r", TEST_DIVISION)
def test_division(x, y, q, r):
    assert x.euclidean_division(y) == (q, r)
    assert x // y == q
    assert x % y == r


TEST_BAD_DIVISION = [
    (
        Polynomials([3, -5, 1, 1], Rationals),
        Rationals(1),
    ),
    (
        Polynomials([3, -5, 1, 1], int),
        Polynomials([-1, 1], int),
    ),
    (
        Polynomials([3, -5, 1, 1], Rationals),
        Polynomials([0, 0], int),
    ),
]


@pytest.mark.parametrize("x,y", TEST_BAD_DIVISION)
def test_bad_division(x, y):
    with pytest.raises((ValueError, TypeError, ZeroDivisionError)):
        x.euclidean_division(y)
    with pytest.raises((ValueError, TypeError, ZeroDivisionError)):
        x // y
    with pytest.raises((ValueError, TypeError, ZeroDivisionError)):
        x % y


TEST_BAD_OPERATIONS = [
    (
        Polynomials([3, -5, 1, 1], Rationals),
        's',
    ),
    (
        's',
        Polynomials([3, -5, 1, 1], Rationals),
    ),
    (
        Polynomials([1, 1], Rationals),
        Polynomials([1, 1], FiveElementsField),
    ),
    (
        Polynomials([1, 1], FiveElementsField),
        Polynomials([1, 1], Rationals),
    ),
    (
        Polynomials([1, 1], Rationals),
        FiveElementsField(1),
    ),
    (
        FiveElementsField(1),
        Polynomials([1, 1], Rationals),
    ),
]


@pytest.mark.parametrize("x,y", TEST_BAD_OPERATIONS)
def test_bad_operations(x, y):
    with pytest.raises((ValueError, TypeError)):
        x + y
    with pytest.raises((ValueError, TypeError)):
        x - y
    with pytest.raises((ValueError, TypeError)):
        x * y
    with pytest.raises((ValueError, TypeError)):
        x // y
    with pytest.raises((ValueError, TypeError)):
        x % y


def test_gcd():
    # Create a list of polynomials (X - i).
    ls = []
    for i in range(6):
        ls.append(Polynomials([-i, 1], Rationals))

    a = ls[0] * ls[0] * ls[0] * ls[0] \
        * ls[1] * ls[1] * ls[1] \
        * ls[2] * ls[2] \
        * ls[3] * ls[3]

    b = ls[1] * ls[1] \
        * ls[2] \
        * ls[4] * ls[4] \
        * ls[5] * ls[5] * ls[5]

    expected = ls[1] * ls[1] * ls[2]
    assert gcd(a, b).to_monic() == expected


TEST_CALL = [
    (
        Polynomials([1, 2, 3, 4, 5], Rationals),
        Polynomials([0, 1], Rationals),
        Polynomials([1, 2, 3, 4, 5], Rationals),
    ),
    (
        Polynomials([-1, 0, 1], Rationals),
        Polynomials([1, 1], Rationals),
        Polynomials([0, 2, 1], Rationals),
    ),
    (
        Polynomials([1, 2, 3, 4, 5], Rationals),
        10,
        54321,
    ),
]


@pytest.mark.parametrize("f,x,expected", TEST_CALL)
def test_call(f, x, expected):
    assert f(x) == expected


TEST_BAD_CALL = [
    (
        Polynomials([1, 1], Rationals),
        's',
    ),
    (
        Polynomials([1, 1], Rationals),
        Polynomials([1, 1], FiveElementsField),
    ),
    (
        Polynomials([1, 1], Rationals),
        FiveElementsField(1),
    ),
    (
        Polynomials([1, 1], Rationals),
        0.0,
    ),
]


@pytest.mark.parametrize("f,x", TEST_BAD_CALL)
def test_bad_call(f, x):
    with pytest.raises((ValueError, TypeError)):
        f(x)
