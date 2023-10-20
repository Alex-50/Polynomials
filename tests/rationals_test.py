import pytest

from rationals import Rationals


TEST_INIT = [
    (3, Rationals(3)),
    (3, Rationals(6, 2)),
    (Rationals(-4, -12), Rationals(2, 6)),
    (Rationals(0, 4), 0.0),
    (Rationals(3, -1), -3),
]


@pytest.mark.parametrize("val,expected", TEST_INIT)
def test_init_and_eq(val, expected):
    assert Rationals(val) == expected


def test_bad_init():
    with pytest.raises(ValueError):
        Rationals('a')
    with pytest.raises(ValueError):
        Rationals(1, 'a')
    with pytest.raises(ValueError):
        Rationals('a', 1)
    with pytest.raises(ValueError):
        Rationals([], {})

    with pytest.raises(ZeroDivisionError):
        Rationals(4, 0)
    with pytest.raises(ZeroDivisionError):
        Rationals(0, 0)


def test_bad_operations():
    with pytest.raises(TypeError):
        Rationals(2, 3) + 'a'
    with pytest.raises(TypeError):
        [] + Rationals(2, 3)

    with pytest.raises(TypeError):
        Rationals(2, 3) - 'a'
    with pytest.raises(TypeError):
        [] - Rationals(2, 3)

    with pytest.raises(TypeError):
        Rationals(2, 3) * 'a'
    with pytest.raises(TypeError):
        [] * Rationals(2, 3)

    with pytest.raises(TypeError):
        Rationals(2, 3) / 'a'
    with pytest.raises(TypeError):
        [] / Rationals(2, 3)


TEST_SUM = [
    (Rationals(3), 5, 8),
    (3, Rationals(5), Rationals(8, 1)),
    (Rationals(1, 6), Rationals(2, 6), Rationals(1, 2)),
    (Rationals(-1, 2), Rationals(2, 4), 0),
    (Rationals(1, 2), 2.0, 2.5),
    (2.0, Rationals(1, 2), 2.5),
]


@pytest.mark.parametrize("a,b,expected", TEST_SUM)
def test_sum(a, b, expected):
    assert a + b == expected


TEST_SUB = [
    (Rationals(3), 5, -2),
    (3, Rationals(5), Rationals(2, -1)),
    (Rationals(1, 6), Rationals(2, 6), -Rationals(1, 6)),
    (Rationals(-1, 2), Rationals(2, 4), -1),
    (Rationals(1, 2), 2.0, -1.5),
    (2.0, Rationals(1, 2), 1.5),
]


@pytest.mark.parametrize("a,b,expected", TEST_SUB)
def test_sub(a, b, expected):
    assert a - b == expected


TEST_MUL = [
    (Rationals(3), 5, 15),
    (3, Rationals(5), Rationals(-15, -1)),
    (Rationals(1, 6), Rationals(2, 6), Rationals(1, 18)),
    (Rationals(-1, 2), Rationals(2, 4), -0.25),
    (Rationals(1, 2), 2.0, 1.0),
    (2.0, Rationals(1, 2), 1.0),
]


@pytest.mark.parametrize("a,b,expected", TEST_MUL)
def test_mul(a, b, expected):
    assert a * b == expected


def test_bad_div():
    with pytest.raises(ZeroDivisionError):
        Rationals(2) / Rationals(0)
    with pytest.raises(ZeroDivisionError):
        0 / Rationals(0, 3)
    with pytest.raises(ZeroDivisionError):
        Rationals(4) / 0
    with pytest.raises(ZeroDivisionError):
        Rationals(4) / 0.0


TEST_DIV = [
    (Rationals(3), 5, Rationals(3, 5)),
    (3, Rationals(5), Rationals(3, 5)),
    (Rationals(1, 6), Rationals(2, 6), Rationals(1, 2)),
    (Rationals(-1, 2), Rationals(2, 4), -1.0),
    (Rationals(1, 2), 2.0, Rationals(1, 4)),
    (2.0, Rationals(1, 2), 4.0),
]


@pytest.mark.parametrize("a,b,expected", TEST_DIV)
def test_div(a, b, expected):
    assert a / b == expected


def test_repr():
    assert repr(Rationals(55, 11)) == "Rationals(5, 1)"
    assert repr(Rationals(3, -6)) == "Rationals(-1, 2)"


def test_str():
    assert str(Rationals(55, 11)) == "5"
    assert str(Rationals(3, -6)) == "-1/2"


TEST_LT = [
    (Rationals(3), 5),
    (3, Rationals(5)),
    (Rationals(1, 6), Rationals(1, 3)),
    (Rationals(-1, 2), -Rationals(1, 4)),
    (Rationals(1, 2), 2.0),
    (2.0, Rationals(5, 2)),
]


@pytest.mark.parametrize("a,b", TEST_LT)
def test_lt(a, b):
    assert a < b


TEST_GE = [
    (5, Rationals(5)),
    (Rationals(5), 3),
    (Rationals(5, 6), Rationals(1, 3)),
    (Rationals(-1, 2), -Rationals(4, 5)),
    (Rationals(1, 2), 0.5),
    (2.0, Rationals(3, 2)),
]


@pytest.mark.parametrize("a,b", TEST_GE)
def test_ge(a, b):
    assert a >= b


def test_bad_cmp():
    with pytest.raises(TypeError):
        Rationals(1, 2) < 's'
    with pytest.raises(TypeError):
        Rationals(1, 2) <= []
    with pytest.raises(TypeError):
        {} < Rationals(1, 2)
    with pytest.raises(TypeError):
        None <= Rationals(1, 2)
