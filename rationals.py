import operator

from abstract_structures import Field
from algorithms import gcd


class Rationals(Field):
    """Residue class of Rational numbers.
    Implements __repr__, __str__, comparison operators.
    """
    _init_exc = ValueError("Rationals() arguments must be an int, 2 ints or an instance of FiveElementsField")
    _zero_exc = ZeroDivisionError("can't divide by zero")

    def _reduce(self):
        """Fractional reduction function """
        if self._denom < 0:
            self._denom *= -1
            self._nom *= -1
        _gcd = gcd(abs(self._nom), self._denom)
        self._nom //= _gcd
        self._denom //= _gcd

    """Initialization is allowed only from an int or an instance of the class."""

    def __init__(self, a, b=1):
        if type(a) is int and type(b) is int:
            if b == 0:
                raise Rationals._zero_exc
            self._nom = a
            self._denom = b
        elif type(a) is Rationals:
            self._nom = a._nom
            self._denom = a._denom
        else:
            raise Rationals._init_exc
        self._reduce()

    """Factory of arithmetic operations"""

    @staticmethod
    def _arithmetic_operator_factory(int_operator):
        def forward(a, b):
            if type(b) is int:
                return Rationals(int_operator(a._nom, b * a._denom), a._denom)
            elif type(b) is float:
                return int_operator(a._nom, b * a._denom) / a._denom
            elif type(b) is Rationals:
                # # # Строки кода должны быть короче 80 символов в длину.
                return Rationals(int_operator(a._nom * b._denom, b._nom * a._denom), a._denom * b._denom)
            return NotImplemented

        def reverse(b, a):
            if type(a) is int:
                return Rationals(int_operator(a * b._denom, b._nom), b._denom)
            elif type(a) is float:
                return int_operator(a * b._denom, b._nom) / b._denom
            elif type(a) is Rationals:
                return Rationals(int_operator(a._nom * b._denom, b._nom * a._denom), a._denom * b._denom)
            return NotImplemented

        return forward, reverse

    __add__, __radd__ = _arithmetic_operator_factory(operator.add)
    __sub__, __rsub__ = _arithmetic_operator_factory(operator.sub)

    """Factory of comparison operations"""

    @staticmethod
    def _comparison_operator_factory(comparison_operator):
        def forward(a, b):
            if type(b) is int or type(b) is float:
                return comparison_operator(a._nom, a._denom * b)
            elif type(b) is Rationals:
                return comparison_operator(a._nom * b._denom, a._denom * b._nom)
            else:
                return NotImplemented

        def reverse(b, a):
            if type(a) is int or type(a) is float:
                return comparison_operator(a * b._denom, b._nom)
            elif type(a) is Rationals:
                return comparison_operator(a._nom * b._denom, b._nom * a._denom)
            else:
                return NotImplemented

        return forward, reverse

    __le__, __ge__ = _comparison_operator_factory(operator.le)
    __lt__, __gt__ = _comparison_operator_factory(operator.lt)
    __eq__, _ = _comparison_operator_factory(operator.eq)

    def __mul__(self, other):
        if type(other) is int:
            return Rationals(self._nom * other, self._denom)
        elif type(other) is float:
            return self._nom * other / self._denom
        elif type(other) is Rationals:
            return Rationals(self._nom * other._nom, self._denom * other._denom)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    """Inverse function"""

    @staticmethod
    def _inverse(a):
        if type(a) in [int, float, Rationals] and a == 0:
            raise Rationals._zero_exc
        if type(a) is int:
            return Rationals(1, a)
        elif type(a) is float:
            return 1 / a
        elif type(a) is Rationals:
            return Rationals(a._denom, a._nom)
        else:
            return NotImplemented

    """a * b = a * (1 / b)"""

    def __truediv__(self, other):
        return self * self._inverse(other)

    def __rtruediv__(self, other):
        return other * self._inverse(self)

    def __neg__(self):
        return Rationals(-self._nom, self._denom)

    def __abs__(self):
        if self._nom < 0:
            return -self
        return self

    def __repr__(self):
        return f"Rationals({self._nom}, {self._denom})"

    def __str__(self):
        if self._denom == 1:
            return f"{self._nom}"
        return f"{self._nom}/{self._denom}"

    def __float__(self):
        return self._nom / self._denom
