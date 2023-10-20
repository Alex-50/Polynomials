import operator
import re
from copy import deepcopy

from abstract_structures import Ring, Field
from integer_residues import FiveElementsField
from rationals import Rationals
import algorithms


class Polynomials(Ring):
    """The ring of polynomials over some Ring R. Inherits Ring.
    Implements __repr__, __str__, __floordiv__, __mod__,
    and __call__.

    Methods:
    degree() -- return the degree of a polynomial (-1 for zero polynomials).
    to_monic() -- return a monic polynomial, which is a scalar multiple of
        the instance.
    shift(n) -- for a positive integer n (or zero), return a polynomial, which is equal
        to the instance multiplied by x^n.
    euclidean_division(divisor) -- for a polynomial with compatible base
        class, return the results of euclidean division of the instance by
        divisor: the integer quotient and the remainder.
    __call__(x) -- return the value of a polynomial in x. x must be either
        cast to base class, or a polynomial over a class, compatible with
        the base class of the instance.
    """
    _init_error_not_polynomial = TypeError(
        "the argument of Polynomials must be an instance of Polynomials"
    )
    _init_error_base_class = TypeError(
        "the base class of Polynomials is not a subclass of Ring"
    )
    _init_error_not_list = TypeError(
        "the first argument of Polynomials is not a list"
    )
    _init_error_cast = TypeError(
        "cannot cast coefficients of Polynomials to the base class"
    )
    _operation_error_cast = TypeError(
        "arithmetic operation between Polynomials with unrelated base classes"
    )
    _operation_error_shift = ValueError(
        "shift(n) can only be called for positive integers n"
    )
    _operation_error_field = TypeError(
        "to_monic(), //, and % can only be done for Polynomials with Field"
        "base classes"
    )
    _operation_error_type = TypeError(
        "arithmetic operation with unknown type"
    )
    _zero_error = ZeroDivisionError(
        "can't divide by zero"
    )

    def __init__(self, values, cls=None):
        """If cls is None, values is a Polynomial, so a copy of values is
        made. Otherwise, cls must be a subclass of Ring, and values must be a
        list of elements of this Ring. So a polynomial f(X) over cls with
        values coefficients is initialized.

        Arguments:
        values -- a list of coefficients of f(X). values[i] is the
            coefficient of X^i.
        cls -- if given, base class for polynomials cls[X]. Must be a
            subclass of Ring.
        """

        # The case of copying another polynomial.
        if cls is None:
            if type(values) is not Polynomials:
                raise self._init_error_not_polynomial
            self._coeffs = deepcopy(values._coeffs)
            self._base_cls = values._base_cls
            return
        """
        Check that cls is subclass of Ring and type(values) is list
        """
        if not issubclass(cls, Ring):
            raise self._init_error_base_class
        if type(values) is not list:
            raise self._init_error_not_list
        _values = deepcopy(values)
        for i in range(len(_values)):
            try:
                _values[i] = cls(_values[i])
            except (ValueError, TypeError):
                raise self._init_error_base_class
        """
        Leading coefficient is not 0 so delete zeros from the end of array
        """
        _values = algorithms.del_extra_zeros(_values)
        self._coeffs = deepcopy(_values)
        self._base_cls = cls

    @staticmethod
    def _operator_factory(polynomial_operator):
        """Construct functions, to assign to methods of arithmetic operations __#__, __r#__.
        This fabric can do __add__, __sub__, __mul__

        __mul__ for polynomials has another logic so it's another function

        Arguments:
        _operator -- an operator for instances of our groups (int, float, Rationals, FiveElementGroup).
        """

        def forward(a, b):
            """a # b"""
            base_cls = a._base_cls
            if type(b) is Polynomials:
                base_cls = algorithms.get_largest_abelian_group(base_cls, b._base_cls, a._operation_error_cast)
            else:
                try:
                    base_cls = algorithms.get_largest_abelian_group(base_cls, type(b), a._operation_error_cast)
                except TypeError:
                    raise a._operation_error_cast
                return Polynomials(polynomial_operator(a._coeffs, [b]), base_cls)
            return Polynomials(polynomial_operator(a._coeffs, b._coeffs), base_cls)

        def reverse(b, a):
            """a # b"""
            base_cls = b._base_cls
            if type(a) is Polynomials:
                base_cls = algorithms.get_largest_abelian_group(base_cls, a._base_cls, b._operation_error_cast)
            else:
                try:
                    base_cls = algorithms.get_largest_abelian_group(base_cls, type(a), b._operation_error_cast)
                except TypeError:
                    raise b._operation_error_cast
                return Polynomials(polynomial_operator([a], b._coeffs), base_cls)
            return Polynomials(polynomial_operator(a._coeffs, b._coeffs), base_cls)

        return forward, reverse

    __add__, __radd__ = _operator_factory(algorithms.add_lists)
    __sub__, __rsub__ = _operator_factory(algorithms.sub_lists)
    __mul__, __rmul__ = _operator_factory(algorithms.mul_lists)

    def __neg__(self):
        """
        Return -self (every element x of coefficients list: x->-x)
        """
        _values = [-i for i in self._coeffs]
        self._coeffs = deepcopy(_values)
        return self

    def degree(self):
        return len(self._coeffs) - 1

    def __eq__(self, other):
        if type(other) is not Polynomials:
            return self._coeffs == Polynomials([other], type(other))._coeffs
        return self._coeffs == other._coeffs and self._base_cls == other._base_cls

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        coeffs = [repr(self._base_cls(i)) for i in self._coeffs]
        return f"Polynomials([{', '.join(coeffs)}], {self._base_cls.__name__})"

    def __str__(self):
        c = deepcopy(self._coeffs)[::-1]
        if not c:
            return str(self._base_cls(0))
        parsed_string = f"{' + '.join([f'{str(a)}*X^{len(c) - i - 1}' for i, a in enumerate(c[:-1]) if a != 0])}"
        if c[-1] != 0:
            parsed_string += f" + {c[-1]}"
        """
        If a[i]<0 then we have '+ -a[i]'
        """
        parsed_string = re.sub(r'\+ -', '- ', parsed_string)
        """
        If there is 1/-1 in coefficients we have '+/- 1X^i'
        """
        parsed_string = re.sub(r'1\*X', 'X', parsed_string)
        """
        There can be 'X^1'
        """
        parsed_string = re.sub('X\^1', 'X', parsed_string)
        return parsed_string

    def shift(self, n: int):
        """Return the instance multiplied by x^n.
        n must be a positive integer or zero.
        """
        # I changed logic a bit :D
        if type(n) is not int or n < 0:
            raise self._operation_error_shift
        _values = [self._base_cls(0) for _ in range(n)]
        _values.extend(deepcopy(self._coeffs))
        return Polynomials(_values, self._base_cls)

    def to_monic(self):
        """Return a monic polynomial, which is a scalar
        multiple of the instance. The base class must be a field.
        """

        """
        As I understood, we shouldn't change self
        """
        if not issubclass(self._base_cls, Field):
            raise self._operation_error_field
        if not self._coeffs:
            return self
        for i in range(len(self._coeffs)):
            self._coeffs[i] = self._base_cls(self._coeffs[i] * (1 / self._coeffs[-1]))
        return self

    def euclidean_division(self, raw_divisor):
        """Return the integer quotient and the remainder of dividing self by
        divisor. Divisor must be a nonzero polynomial.
        """
        if type(raw_divisor) is not Polynomials:
            raise self._operation_error_type
        if raw_divisor == 0:
            raise self._zero_error
        if self._base_cls == raw_divisor._base_cls == int:
            raise self._operation_error_cast
        base_cls = algorithms.get_largest_abelian_group(self._base_cls, raw_divisor._base_cls,
                                                        self._operation_error_cast)
        if Rationals in [self._base_cls, raw_divisor._base_cls]:
            base_cls = Rationals
        quotient = Polynomials([], base_cls)
        _raw_divisor = Polynomials(deepcopy(raw_divisor._coeffs), base_cls)
        """
        I'm going to change coeeficients of self so I make a copy of it
        """
        _self = deepcopy(self)
        _self._base_cls = base_cls
        while _self.degree() >= _raw_divisor.degree():
            k = _self._coeffs[-1] * (1 / _raw_divisor._coeffs[-1])
            deg = _self.degree() - _raw_divisor.degree()
            quotient = quotient + Polynomials([k], base_cls).shift(deg)
            _self = Polynomials(_self - k * _raw_divisor.shift(deg))
        return quotient, _self

    def __floordiv__(self, other):
        """Return the integer quotient of dividing self by
        other. other must be a nonzero polynomial.
        """
        return self.euclidean_division(other)[0]

    def __mod__(self, other):
        """Return the remainder of dividing self by
        other. other must be a nonzero polynomial.
        """
        return self.euclidean_division(other)[1]

    def __call__(self, val):
        """Return the value of f(val)."""

        """
        According to my code, we can do float(Rationals)
        but since it's illegal, there is an 'if' under comment.
        """
        if self._base_cls is Rationals and type(val) is float:
            raise self._operation_error_cast
        if type(val) is Polynomials:
            try:
                cls = algorithms.get_largest_abelian_group(self._base_cls, val._base_cls,
                                                           self._operation_error_cast)
            except:
                raise self._operation_error_type
        else:
            try:
                cls = algorithms.get_largest_abelian_group(self._base_cls, type(val),
                                                           self._operation_error_cast)
            except:
                raise self._operation_error_type
        ans = Polynomials([], self._base_cls)
        for i in self._coeffs[::-1]:
            ans = ans * val
            ans = ans + i
        return ans
