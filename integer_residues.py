import operator

from abstract_structures import Field


class ThreeElementsField(Field):
    """Residue class field Z / 3Z. Inherits Field.
    Implements __repr__ and __str__.
    """
    _init_exc = ValueError("ThreeElementsField() argument must be an int or an instance of ThreeElementsField")
    _zero_exc = ZeroDivisionError("can't divide by zero")
    _prime = 3

    def __init__(self, num):
        """Initialization is allowed only from an int or an instance of the class."""

        # _value is always the unique residue in segment [0, 2].
        if type(num) is int:
            self._value = num % ThreeElementsField._prime
        elif isinstance(num, ThreeElementsField):
            self._value = num._value
        else:
            raise ThreeElementsField._init_exc

    @staticmethod
    def _operator_factory(int_operator):
        """Construct functions, to assign to methods of arithmetic operations __#__, __r#__.

        Arguments:
        int_operator -- an operator for ints. It's applied to _value.
        """

        def forward(a, b):
            """a # b"""
            if type(b) is int:
                return ThreeElementsField(int_operator(a._value, b))
            if isinstance(b, ThreeElementsField):
                return ThreeElementsField(int_operator(a._value, b._value))
            return NotImplemented

        def reverse(b, a):
            """a # b"""
            if type(a) is int:
                return ThreeElementsField(int_operator(a, b._value))
            if isinstance(a, ThreeElementsField):
                return ThreeElementsField(int_operator(a._value, b._value))
            return NotImplemented

        return forward, reverse

    __add__, __radd__ = _operator_factory(operator.add)

    def __neg__(self):
        return ThreeElementsField(-self._value)

    __sub__, __rsub__ = _operator_factory(operator.sub)

    def __eq__(self, other):
        if type(other) is int:
            return self._value == (other % ThreeElementsField._prime)
        if isinstance(other, ThreeElementsField):
            return self._value == other._value
        return NotImplemented

    __mul__, __rmul__ = _operator_factory(operator.mul)

    @staticmethod
    def _truediv(a: int, b: int):
        if b % ThreeElementsField._prime == 0:
            raise ThreeElementsField._zero_exc
        return a * b

    __truediv__, __rtruediv__ = _operator_factory(_truediv)

    def __repr__(self):
        return f"ThreeElementsField({self._value})"

    def __str__(self):
        return '_' + str(self._value) + '_'


class FiveElementsField(Field):
    """Residue class field Z / 5Z. Inherits Field.
    Implements __repr__ and __str__.
    """
    _init_exc = ValueError("FiveElementsField() argument must be an int or an instance of FiveElementsField")
    _zero_exc = ZeroDivisionError("can't divide by zero")
    _prime = 5

    def __init__(self, num):
        """Initialization is allowed only from an int or an instance of the class."""

        # _value is always the unique residue in segment [0, 4].
        if type(num) is int:
            self._value = num % FiveElementsField._prime
        elif type(num) is FiveElementsField:
            self._value = num._value
        else:
            raise FiveElementsField._init_exc

    @staticmethod
    def _operator_factory(int_operator):
        """Construct functions, to assign to methods of arithmetic operations __#__, __r#__.

        Arguments:
        int_operator -- an operator for ints. It's applied to _value.
        """
        def forward(a, b):
            """a # b"""
            if type(b) is int:
                return FiveElementsField(int_operator(a._value, b))
            if type(b) is FiveElementsField:
                return FiveElementsField(int_operator(a._value, b._value))
            return NotImplemented

        def reverse(b, a):
            """a # b"""
            if type(a) is int:
                return FiveElementsField(int_operator(a, b._value))
            if type(a) is FiveElementsField:
                return FiveElementsField(int_operator(a._value, b._value))
            return NotImplemented

        return forward, reverse

    __add__, __radd__ = _operator_factory(operator.add)
    __mul__, __rmul__ = _operator_factory(operator.mul)
    __sub__, __rsub__ = _operator_factory(operator.sub)

    def __neg__(self):
        return FiveElementsField(-self._value)

    @staticmethod
    def _truediv(a: int, b: int):
        if b % FiveElementsField._prime == 0:
            raise FiveElementsField._zero_exc
        return a * (b ** 3)

    __truediv__, __rtruediv__ = _operator_factory(_truediv)

    def __eq__(self, other):
        if type(other) is int:
            return self._value == other % FiveElementsField._prime
        elif type(other) is FiveElementsField:
            return self._value == other._value
        return NotImplemented

    def __repr__(self):
        return f"FiveElementsField({self._value})"

    def __str__(self):
        return '_' + str(self._value) + '_'

    def __int__(self):
        return self._value
