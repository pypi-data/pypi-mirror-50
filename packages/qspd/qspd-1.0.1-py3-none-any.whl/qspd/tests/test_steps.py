import unittest
from collections import defaultdict
from fractions import Fraction
from random import randint

from mpmath import fabs, ldexp, matrix, norm, ln, ceil
from mpmath import mp, rand, erfinv, fdiv, fmul, fsub, almosteq, nstr
from mpmath import mpc, expj, mpf, pi
from sympy import Matrix, zeros

from qspd import step1, InputFunction, Parity, step2, step4, step3
from qspd.tests import recompose
from qspd.util import rational_to_mpc, polyval_dict, ImaginaryRational


# Tests steps 1 - 5 individually or in small groups
# Run this script to perform unit testing.
class UnitTesting(unittest.TestCase):
    def test_step1(self):
        for j in range(50):
            mp.dps = 150
            big_n = randint(1, 20)
            big_a, big_b = defaultdict(lambda: mpf(0)), defaultdict(lambda: mpc(0))
            for i in range(big_n + 1):
                # citation:
                # https://docs.sympy.org/0.7.1/modules/mpmath/functions/expintegrals.html#erfinv
                a_i, b_i = erfinv(2 * rand() - 1), mpc(0, erfinv(2 * rand() - 1))
                big_a[i], big_a[-i] = a_i, a_i
                if i != 0:
                    big_b[i], big_b[-i] = b_i, -b_i
            epsilon = mpf(10) ** randint(-10, -3)
            epsilon_over_n = fdiv(epsilon, big_n, rounding='u')
            one_minus_five_epsilon = fsub(1, fmul(5, epsilon, exact=True), exact=True)
            big_a = InputFunction(big_a, Parity.EVEN, big_n)
            big_b = InputFunction(big_b, Parity.ODD, big_n)
            a, b, n = step1(big_a, big_b, epsilon)

            mp.dps = 150

            def test_coefficient(big_p, p, i):
                expected = fmul(one_minus_five_epsilon, big_p[i], exact=True)
                actual = rational_to_mpc(p[i])
                are_equal = almosteq(expected, actual, abs_eps=epsilon_over_n)
                if not are_equal:
                    print(f"expected: {nstr(expected, n=10)} but was: {nstr(actual, n=10)}")
                self.assertTrue(are_equal)

            for i in range(n):
                test_coefficient(big_a, a, i)
                test_coefficient(big_b, b, i)
                self.assertEqual(a[i], a[-i])
                self.assertEqual(b[i], -b[-i])

    def test_step2(self):
        # Step 1: Construct the inputs to step2()
        n = 5
        mp.dps = 150

        def im(x):
            return ImaginaryRational(x)

        a_coeffs = [(-5, 1), (-4, 1), (-3, 1), (-2, 4), (-1, 5), (0, Fraction(6, 5)), (1, 1),
                    (2, 4), (3, -4),
                    (4, -1), (5, 0)]  # a has real coeffs
        b_coeffs = [(-5, im(0)), (-4, im(1)), (-3, im(2)), (-2, im(3)), (-1, im(4)), (0, im(5)),
                    (1, im(-4)),
                    (2, im(-3)), (3, im(-3)), (4, im(-1)), (5, im(0))]  # b has imaginary coeffs

        # construct a dict from the coeffs in a_list and b_list
        a = defaultdict(lambda: 0)
        b = defaultdict(lambda: 0)
        for key, value in a_coeffs:
            a[key] = value
        for key, value in b_coeffs:
            b[key] = value

        # Outputs of step2()
        p, roots = step2(a, b, n)

        # Step 3: Check that p is the correct polynomial
        radius = 3  # inputs range from -radius to radius
        step_size = mpf(1) / 5  # number of points along one coordinate from 0 to radius

        num = int(radius / step_size)
        for alpha in range(-num, num + 1):
            for beta in range(-num, num + 1):
                z = mpc(alpha, beta) * step_size  # the complex value input into a, b, and p
                if z == mpc(0, 0):
                    continue

                a_z = polyval_dict(a, z)  # the value of a evaluated at z
                b_z = polyval_dict(b, z)
                p_z = polyval_dict(p, z)

                err = fabs(p_z - (1 - a_z ** 2 - b_z ** 2))  # absolute error
                self.assertLessEqual(err, ldexp(1, -15))  # err <= 2^-15

        # Step 4: Check that the roots are correct
        for r in roots:
            err = fabs(polyval_dict(p, r))  # absolute error
            self.assertLessEqual(err, ldexp(1, -15))  # err <= 2^-15
        self.assertTrue(True)  # does nothing

    def test_step4(self):
        # Step 1: Define a Laurent polynomial whose coeffs are 2x2 matrices
        coeffs = defaultdict(lambda: zeros(2))  # the coeffs of a Laurent polynomial
        coeffs[-1] = Matrix([[mpc(0, 1), 0], [mpc(2, .3), 1]])
        coeffs[0] = Matrix([[1, 0], [0, 1]])
        coeffs[1] = Matrix([[1, 0], [0, 2]])
        coeffs[2] = Matrix([[mpc(1, 2), 1], [mpc(4, 1.7), 0]])

        # Step 2: Evaluate the polynomial on at least 2n+1 inputs
        n = max(abs(j) for j in coeffs.keys())  # the degree of the Laurent polynomial
        d = 2 ** ((2 * n + 1).bit_length())  # number of inputs
        F = []  # the value of the polynomial at each input

        for k in range(d):
            z = expj(2 * pi * mpf(k) / d)  # the input value
            F_z = zeros(2)  # the function's output
            for power in coeffs:
                F_z += coeffs[power] * (z ** power)
            F.append(F_z)

        # Step 3: Recover the coeffs by taking the FFT of vals
        fft_coeffs = step4(F, n)

        # Check that fft_coeffs are close to coeffs
        for i in fft_coeffs.keys():
            err = norm(fft_coeffs[i] - matrix(coeffs[i / 2]))
            self.assertLessEqual(err, ldexp(1, -15))  # err <= 2^-15

    def test_step3_4(self):
        """
        Test step4() using the output of step3().
        Treat the coeffs output by step4() as a function. Compute the value of this function for many inputs.
        The function values should match the values output by step3().
        """
        # Step 1: Perform steps 1-4 on random input (code taken from main.py)
        mp.dps = 150
        epsilon = 0.0001  # precision control, epsilon should be between 0 and 1
        angles, big_a, big_b = _recompose_random(2)
        a, b, n = step1(big_a, big_b, epsilon)
        p, roots = step2(a, b, n)
        F = step3(a, b, n, p, roots)
        fft_coeffs = step4(F, n)

        # Step 2: Compute the values of function F using the coeffs given by step 4
        d = len(F)  # number of function values to compute
        F_est = []  # the estimated function values
        for k in range(d):
            z = expj(2 * pi * mpf(k) / mpf(d))  # the input value
            F_z = matrix(zeros(2))  # the function's output
            for power in fft_coeffs:
                F_z += fft_coeffs[power] * (z ** (power / 2))
            F_est.append(F_z)

        # Step 3: Compare the values in F and est_F
        for i in range(d):
            err = norm(F_est[i] - matrix(F[i].evalf()))
            self.assertLessEqual(err, ldexp(1, -15))  # err <= 2^-15

    def test_step1_2_3(self):
        """
        Check that steps 1-3 compute the correct function F.
        The input to step1() is a function, described by big_a and big_b: f(t) = big_a(t^2) + i * big_b(t^2).
        Compute the value of this function over many inputs.
        Then check that f(t^2) = <+|F(t)|+> for these inputs, where F(t) is the output of step3().
        """
        # Step 1: Generate an input to step1().
        epsilon = ldexp(1, -150)  # precision control, epsilon should be between 0 and 1
        angles, big_a, big_b = _recompose_random(3)
        big_n = max(big_a.degree, big_b.degree)
        mp.dps = int(ceil((big_n / 3) * ln(big_n / epsilon)))

        f = defaultdict()  # f(z) = big_a(z) + i * big_b(z)
        for i in range(-big_n, big_n + 1):
            f[i] = big_a[i] + mpc(0, 1) * big_b[i]

        # Step 2: Execute steps 1-3 to get function values of F(t)
        def sum_div_2(mat):
            """
            :param mat: a 2x2 matrix
            :return: the sum of the four elements of the matrix, divided by 2
            This is equivalent to: <+|mat|+>
            """
            return (mat[0, 0] + mat[0, 1] + mat[1, 0] + mat[1, 1]) / 2

        a, b, n = step1(big_a, big_b, epsilon)
        p, roots = step2(a, b, n)
        F = step3(a, b, n, p, roots)  # the coeffs of F(z)
        F1 = [sum_div_2(matrix(F[i])) for i in range(len(F))]  # F_1(z) = <+|F(z)|+>

        # Step 3: Check that <+|F(z)|+> = f(z)
        d = len(F1)  # number of inputs to test
        for k in range(d):
            z = expj(2 * pi * mpf(k) / d)  # the input value
            f_z = polyval_dict(f, z)  # f(z)

            err = fabs(F1[k] - f_z)  # /fabs(f_val)
            self.assertLessEqual(err, ldexp(1, -15))  # err <= 2^-15


def _recompose_random(n):
    """
    Performs reverse_decomp on a random set of 2n+1 angles
    :param n: the degree of the resulting function, A(z) + iB(z), assuming no terms cancel
    :return: the list of 2n+1 random angles, the functions A(z) and B(z), as FloatFunctions,
            and the degree, big_n, of the functions
    """
    angles = [rand() * 2 * pi for _ in range(2 * n + 1)]
    a, b = recompose(angles)
    return angles, a, b


if __name__ == '__main__':
    unittest.main()
