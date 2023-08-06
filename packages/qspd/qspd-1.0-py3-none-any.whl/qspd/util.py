from enum import Enum
from fractions import Fraction
from numbers import Rational

from mpmath import mpf, mpc, fadd, fsub, fmul, fdiv, fraction, fsum


class ImaginaryRational:
    """
    A rational number multiplied by i. Squaring an ImaginaryRational will yield a negative Fraction.
    """

    def __new__(cls, numerator=0, denominator=None):
        self = super(ImaginaryRational, cls).__new__(cls)
        self._value = Fraction(numerator, denominator)
        return self

    @property
    def value(self):
        return self._value

    @property
    def numerator(self):
        return self._value.numerator

    @property
    def denominator(self):
        return self._value.denominator

    # repr(self)
    def __repr__(self):
        return f"ImaginaryRational({self.numerator}, {self.denominator})"

    # str(self)
    def __str__(self):
        return f"{self.numerator}i/{self.denominator}"

    # self + other
    def __add__(self, other):
        if other == 0:
            return self
        if isinstance(other, ImaginaryRational):
            return ImaginaryRational(self.value + other.value)
        elif isinstance(other, (mpf, mpc)):
            return fadd(self.mpc, other)
        if isinstance(other, Rational) and self.value == 0:
            return other
        return NotImplemented

    # other + self
    def __radd__(self, other):
        return self + other

    # self - other
    def __sub__(self, other):
        if other == 0:
            return self
        if isinstance(other, ImaginaryRational):
            return ImaginaryRational(self.value - other.value)
        elif isinstance(other, (mpf, mpc)):
            return fsub(self.mpc, other)
        if isinstance(other, Rational) and self.value == 0:
            return other
        return NotImplemented

    # other - self
    def __rsub__(self, other):
        if other == 0:
            return ImaginaryRational(-self.value)
        if isinstance(other, ImaginaryRational):
            return ImaginaryRational(other.value - self.value)
        elif isinstance(other, (mpf, mpc)):
            return fsub(other, self.mpc)
        if isinstance(other, Rational) and self.value == 0:
            return other
        return NotImplemented

    # self * other
    def __mul__(self, other):
        if other == 0:
            return 0
        if isinstance(other, Rational):
            return ImaginaryRational(self.value * other)
        elif isinstance(other, ImaginaryRational):
            return Fraction(-self.value * other.value)
        elif isinstance(other, (mpf, mpc)):
            return fmul(other, self.mpc)
        return NotImplemented

    # other * self
    def __rmul__(self, other):
        return self * other

    # self / other
    def __truediv__(self, other):
        if isinstance(other, Rational):
            return ImaginaryRational(self.value / other)
        if isinstance(other, ImaginaryRational):
            return Fraction(self.value / other.value)
        elif isinstance(other, (mpf, mpc)):
            return fdiv(self.mpc, other)
        return NotImplemented

    # other / self
    def __rtruediv__(self, other):
        if isinstance(other, Rational):
            return ImaginaryRational(-other / self.value)
        elif isinstance(other, ImaginaryRational):
            return Fraction(other.value / self.value)
        elif isinstance(other, (mpf, mpc)):
            return fdiv(other, self.mpc)
        return NotImplemented

    # self ** power
    def __pow__(self, power):
        if not isinstance(power, int):
            return NotImplemented
        result = self.value ** power
        power_mod_4 = power % 4
        if power_mod_4 == 0:
            return Fraction(result)
        elif power_mod_4 == 1:
            return ImaginaryRational(result)
        elif power_mod_4 == 2:
            return Fraction(-result)
        else:
            assert power_mod_4 == 3
            return ImaginaryRational(-result)

    # +self
    def __pos__(self):
        return self

    # -self
    def __neg__(self):
        return ImaginaryRational(-self.value)

    # abs(self)
    def __abs__(self):
        return abs(self.value)

    # hash(self)
    def __hash__(self):
        value = self.value
        if value == 0:
            return hash(0)
        return 13 + hash(self.value)

    # self == other
    def __eq__(self, other):
        value = self.value
        if value == 0 and other == 0:
            return True
        if not isinstance(other, ImaginaryRational):
            return False
        return value == other.value

    def __bool__(self):
        return self.value != 0

    @property
    def mpc(self):
        return mpc(0, fraction(self.numerator, self.denominator))


class Parity(Enum):
    """
    The parity of a function, either even or odd.
    """
    ODD = 1
    EVEN = 2


# TODO refactor InputFunction
# a function, with definite parity and coefficients accessible via indexing
class InputFunction:
    """
    A function that can be input to Haah's algorithm. This function can be thought of as a
    2pi-periodic function applied to real numbers, represented in terms of its Fourier coefficients,
    or it can be thought of as a Laurent polynomial
    """
    def __init__(self, coefficients, parity, degree=None):
        self._coefficients = coefficients
        self.parity = parity
        if degree is None:
            powers = (abs(power) for power, coefficient in coefficients.items() if coefficient != 0)
            self.degree = max(powers, default=0)
        else:
            self.degree = degree

    def __getitem__(self, item):
        return self._coefficients.get(item, mpf(0))

    def __iter__(self):
        return iter(range(-self.degree, self.degree + 1))

    def __str__(self):
        return str(dict(self._coefficients))

    def __repr__(self):
        return repr(dict(self._coefficients))


def rational_to_mpc(x):
    """
    Produces an mpmath floating-point number with a zero real part and an imaginary part
    approximately equal to the value of the parameter

    :param x: a number, either Rational or ImaginaryRational
    :return: an mpf or mpc approximation to the parameter
    """
    if isinstance(x, Rational):
        return fraction(x.numerator, x.denominator)
    elif isinstance(x, ImaginaryRational):
        return x.mpc
    raise TypeError


def polyval_dict(coeffs, x):
    """
    Evaluates a Laurent polynomial at a particular value. This function can be represented as a
    dictionary with rational or floating-point coefficients, or as a FloatFunction.

    :param coeffs: the coefficients, indexed by power
    :param x: an mpmath.mpc complex value at which to evaluate the function
    :return:
    """
    def eval_term(power):
        coeff = coeffs[power]
        if isinstance(coeff, (Rational, ImaginaryRational)):
            return rational_to_mpc(coeff) * x ** power
        else:
            return coeff * x ** power

    return fsum(eval_term(power) for power in coeffs)
