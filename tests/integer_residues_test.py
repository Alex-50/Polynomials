import pytest

from integer_residues import FiveElementsField

TEST_INIT = [
    (15, FiveElementsField(0)),
    (3, FiveElementsField(-2)),
    (FiveElementsField(7), FiveElementsField(2)),
    (FiveElementsField(4), -1),
]


@pytest.mark.parametrize("val,expected", TEST_INIT)
def test_init_and_eq(val, expected):
    assert FiveElementsField(val) == expected


def test_bad_init():
    with pytest.raises(ValueError):
        FiveElementsField(0.0)


def test_bad_operations():
    with pytest.raises(TypeError):
        FiveElementsField(2) + 'a'
    with pytest.raises(TypeError):
        [] + FiveElementsField(2)

    with pytest.raises(TypeError):
        FiveElementsField(2) - 'a'
    with pytest.raises(TypeError):
        [] - FiveElementsField(2)

    with pytest.raises(TypeError):
        FiveElementsField(2) * 'a'
    with pytest.raises(TypeError):
        [] * FiveElementsField(2)

    with pytest.raises(TypeError):
        FiveElementsField(2) / 'a'
    with pytest.raises(TypeError):
        [] / FiveElementsField(2)


TEST_SUM = [
    (FiveElementsField(0), 5, 0),
    (3, FiveElementsField(4), FiveElementsField(2)),
    (FiveElementsField(2), FiveElementsField(-2), FiveElementsField(0)),
    (FiveElementsField(-1), FiveElementsField(-3), 1),
]


@pytest.mark.parametrize("a,b,expected", TEST_SUM)
def test_sum(a, b, expected):
    assert a + b == expected


TEST_SUB = [
    (FiveElementsField(0), 5, 0),
    (3, FiveElementsField(4), FiveElementsField(4)),
    (FiveElementsField(2), FiveElementsField(-2), FiveElementsField(4)),
    (FiveElementsField(-1), FiveElementsField(-3), 2),
]


@pytest.mark.parametrize("a,b,expected", TEST_SUB)
def test_sub(a, b, expected):
    assert a - b == expected


TEST_MUL = [
    (FiveElementsField(0), 5, 0),
    (3, FiveElementsField(4), FiveElementsField(2)),
    (FiveElementsField(2), FiveElementsField(-2), FiveElementsField(1)),
    (FiveElementsField(-1), FiveElementsField(-3), 3),
]


@pytest.mark.parametrize("a,b,expected", TEST_MUL)
def test_mul(a, b, expected):
    assert a * b == expected


def test_bad_div():
    with pytest.raises(ZeroDivisionError):
        FiveElementsField(2) / FiveElementsField(5)
    with pytest.raises(ZeroDivisionError):
        0 / FiveElementsField(-5)
    with pytest.raises(ZeroDivisionError):
        FiveElementsField(4) / 0


TEST_DIV = [
    (FiveElementsField(0), 4, 0),
    (3, FiveElementsField(4), FiveElementsField(-3)),
    (FiveElementsField(2), FiveElementsField(-2), FiveElementsField(-1)),
    (FiveElementsField(-1), FiveElementsField(-3), 2),
]


@pytest.mark.parametrize("a,b,expected", TEST_DIV)
def test_div(a, b, expected):
    assert a / b == expected


def test_repr():
    assert repr(FiveElementsField(55)) == "FiveElementsField(0)"
    assert repr(FiveElementsField(-1)) == "FiveElementsField(4)"


def test_str():
    assert str(FiveElementsField(55)) == "_0_"
    assert str(FiveElementsField(-1)) == "_4_"
