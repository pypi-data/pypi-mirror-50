from collections import defaultdict
from fractions import Fraction

from mpmath import fdiv, fmul, fsub, floor, frac, fneg, almosteq, mp, ldexp, fadd, fraction, \
    polyroots, sqrt, fabs, mpc, expjpi, mpf, matrix, zeros, chop, eig, eye, polar, pi
from sympy import symbols, Matrix, I, fft

from qspd.util import ImaginaryRational, Parity, polyval_dict


def step1(big_a, big_b, epsilon, forced_n=None):
    if forced_n is None:
        big_n = max(big_a.degree, big_b.degree)
    else:
        big_n = forced_n

    # epsilon divided by n, used for precision
    epsilon_over_big_n = fdiv(epsilon, big_n, rounding='d')
    one_minus_five_epsilon = fsub(1, fmul(5, epsilon, exact=True), exact=True)

    # separates a floating-point number into integer and fractional parts
    def extract(x):
        return int(floor(x)), frac(x)

    # finds the "best" rational number between the two given floating-point numbers
    # based on https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_within_an_interval
    def rational_within_range(x, y):
        x_int, x_frac = extract(x)
        y_int, y_frac = extract(y)
        if x_int == y_int:
            if x_frac == 0 or y_frac == 0:
                return x_int
            assert x_frac != y_frac
            if x_frac < y_frac:
                x_frac_inv = fdiv(1, x_frac, rounding='d')
                y_frac_inv = fdiv(1, y_frac, rounding='u')
            else:
                x_frac_inv = fdiv(1, x_frac, rounding='u')
                y_frac_inv = fdiv(1, y_frac, rounding='d')
            frac_rat = Fraction(1, rational_within_range(x_frac_inv, y_frac_inv))
            return x_int + frac_rat
        else:
            return min(x_int, y_int) + 1

    # converts a floating-point number to a rational number
    def float_to_rational(x):
        if x < 0:
            return -float_to_rational(fneg(x, exact=True))
        if almosteq(x, 0, abs_eps=epsilon_over_big_n):
            if forced_n is None or x == 0:
                return 0
        min_result = fsub(x, epsilon_over_big_n, rounding='u')
        if min_result <= 0:
            min_result = ldexp(1, -mp.dps)
        max_result = fadd(x, epsilon_over_big_n, rounding='d')
        return rational_within_range(min_result, max_result)

    # converts a Fourier coefficient from the original floating-point number to a rational one
    def convert_coefficient(x):
        complex_result = fmul(one_minus_five_epsilon, x, exact=True)
        real, imag = complex_result.real, complex_result.imag
        if imag == 0:
            return float_to_rational(real)
        elif real == 0:
            return ImaginaryRational(float_to_rational(imag))
        raise ValueError

    # converts each coefficient in the function, also returning the new number of coefficients
    def convert_function(f):
        parity = f.parity
        coefficients = defaultdict(lambda: 0)
        new_n = 0
        for i in range(0, big_n + 1):
            converted = convert_coefficient(f[i])
            if converted == 0:
                continue
            new_n = i
            coefficients[i] = converted
            if parity == Parity.EVEN:
                coefficients[-i] = converted
            else:
                coefficients[-i] = -converted
        return coefficients, new_n

    a, n_a = convert_function(big_a)
    b, n_b = convert_function(big_b)
    return a, b, max(n_a, n_b)


def step2(a, b, n):
    """
    :param a: (dicts of rational) the coeffs of a(z)
    :param b: (dicts of rational) the coeffs of b(z)
    :param n: (int) the max degree of a or b (computed in step 1)
    :param epsilon: related to the precision of the computations
    :return: p (dict of rationals): the coefficients of p(z) =  = 1 - a(z)^2 - b(z)^2
             roots (list of floats): the roots of p(z)
    """

    # Step 1: Compute the coeffs of a(t)^2 and b(t)^2
    def square_poly(f):
        """
        :param f: (defaultdict) the coeffs of polynomial f(t)
        :return: the coeffs of f(t)^2
        """
        result = {}
        for i in range(-2 * n, 2 * n + 1):  # range = [-2n, 2n]
            lo = max(i - n, -2 * n)  # lo and hi give the range of coeffs to sum over
            hi = min(i + n, 2 * n)
            result[i] = sum(f[j] * f[i - j] for j in range(lo, hi + 1))
        return result

    a2, b2 = square_poly(a), square_poly(b)  # a2 and b2 give the coeffs of a(t)^2 and b(t)^2

    # Step 2: Compute the coeffs of p = 1 - a^2 - b^2
    p = {i: -(a2[i] + b2[i]) for i in range(-2 * n, 2 * n + 1)}  # the coeffs of polynomial p
    p[0] += 1

    def to_mpf(x):
        return fraction(x.numerator, x.denominator)

    # Step 3: Find the roots of p
    max_degree = max(k for k in p.keys() if p[k] != 0)  # max degree of any term in p
    min_degree = min(k for k in p.keys() if p[k] != 0)  # min degree of any term in p
    max_steps = n ** 3 + n ** 2 * mp.prec + 50  # a bit overkill
    if all(v == 0 or k % 2 == 0 for k, v in p.items()):
        coeff_list = [to_mpf(p[i]) for i in range(max_degree, min_degree - 1, -2)]
        squared_roots = polyroots(coeff_list, maxsteps=max_steps)
        roots = []
        for r in squared_roots:
            sqrt_r = sqrt(r)
            roots.append(sqrt_r)
            roots.append(-sqrt_r)
    else:
        # Note: the highest-degree terms come first in p (ex: p[0] corresponds to the 2n-degree term)
        # the coeffs of polynomial p, stored in a list and expressed as floats (mpf)
        coeff_list = [to_mpf(p[i]) for i in range(max_degree, min_degree - 1, -1)]
        roots = polyroots(coeff_list, maxsteps=max_steps)
    return p, roots


#  Evaluating complementary polynomials c(z) and d(z) at T = {exp(2 pi i k / D) | k = 1,...,D}
#  D is a power of 2 that is larger than 2n+1
#  n is degree of input polynomials that have been reduced from coefficient approximation
#  roots is a list of roots of the polynomial 1 - a(z)^2 - b(z)^2
#  poly_dict is a dictionary of coefficients of the polynomial 1 - a(z)^2 - b(z)^2
#  a_dict and b_dict are polynomials a(z) and b(z) represented as dicts of coefficients
#  Can set ret_alpha to True if wanted to return both F and alpha, alpha is used for testing the midpoint of step 3
#  RETURNS F evaluated at points of T described above, as 4 lists
def step3(a, b, n, p, roots, big_r_1=None, big_r_2=None):
    big_c = [r for r in roots if r.imag > 0 and abs(r) < 1]
    if big_r_1 is None or big_r_2 is None:
        big_r = [r.real for r in roots if r.imag == 0 and abs(r) < 1]
        if big_r_1 is not None:
            big_r_2 = list(big_r)
            for r in big_r_1:
                big_r_2.remove(r)
        elif big_r_2 is not None:
            big_r_1 = list(big_r)
            for r in big_r_2:
                big_r_1.remove(r)
        else:
            big_r.sort(reverse=True)
            len_big_r_1 = len(big_r) // 2
            big_r_1 = big_r[:len_big_r_1]
            big_r_2 = big_r[len_big_r_1:]

    # Step 1: Build e(z) and e(1/z) symbolically, as described in eq. 13
    z = symbols("z")
    e_z = 1  # starts as multiplication identity
    for r in big_c:
        e_z *= z - 2 * r.real + (fabs(r) ** 2) / z
    for r in big_r_1:
        e_z *= z - r
    for r in big_r_2:
        e_z *= 1 / z - r

    e_1_z = e_z.subs(z, (1 / z))  # e(1/z)

    alpha_num = polyval_dict(p, mpc(1))  # evaluating at z = 1
    alpha_denom = e_z * e_1_z  # e(z)*e(1/z)  # symbolic expression
    alpha_denom = alpha_denom.evalf(subs={z: 1})  # evaluate at z = 1
    alpha = mpc(alpha_num / alpha_denom)  # a real alpha, We think alpha is constant for all z

    # Step 2: Compute F(t) for various inputs of t on the unit circle
    F = []  # stores the value of F(z) for various inputs z

    # Pauli Matrices (used below to compute F)
    Id = Matrix([[1, 0], [0, 1]])  # 2 x 2 identity matrix
    X = Matrix([[0, 1], [1, 0]])
    Y = Matrix([[0, -1 * I], [I, 0]])
    Z = Matrix([[1, 0], [0, -1]])

    # evaluates e(z), a(z), b(z), c(z), d(z), and F(z) over a set of d inputs, called x.
    d = 2 ** ((2 * n + 1).bit_length())  # next power of 2 greater than 2n + 1
    for k in range(d):  # [0, D - 1]
        x = expjpi(2 * mpf(k) / mpf(d))  # the input value (from eq. 15)

        # Compute the values of e(x), e_inv(x), a(x), b(x), c(x), d(x), and F(x)
        e_x = e_z.evalf(subs={z: x})  # e(x)
        e_1_x = e_1_z.evalf(subs={z: x})  # e(1/x)

        # note that c_x and d_x are switched.
        a_x = polyval_dict(a, x)  # a(x)
        b_x = polyval_dict(b, x)  # b(x)
        c_x = (e_x - e_1_x) * sqrt(alpha) / mpc(2j)  # c(x)
        d_x = (e_x + e_1_x) * sqrt(alpha) / mpf(2)  # d(x)

        F.append(a_x * Id + b_x * I * X + c_x * I * Y + d_x * I * Z)

    return F


def step4(f, n):
    """
    Computes the FFT of f and returns a dict, c, of matrices.
    :param f: (list of 2 x 2 Sympy Matrices) the values of F(x), computed over a set of inputs in step3()
    :param n: (int) max. degree of a(z) or b(z) (computed in step_1())
    :return: c (dict of 2 x 2 mpmath matrices): the coefficients of F(z)
    """
    # Take the FFT of the f-values to find the matrices C.
    c_list = fft(f, dps=mp.dps)  # the C matrices, the Laurent coeffs of F(z)

    # Invert c_list: fft returns the matrix C_j as element c_list[-j]. We don't know why.
    c_list = [c_list[-i] for i in range(len(c_list))]
    c_list = [(matrix(c_list[i].evalf())) for i in range(len(c_list))]  # convert to mpmath matrices

    # Convert c_list to a dict with appropriate indexing
    d = len(f)
    c = defaultdict(lambda: zeros(2))  # stores the entries of c_list as a dict

    for i in range(-n, 0):  # {-n, -n + 1, ..., -1}
        c[2 * i] = c_list[i + d] / d  # set the coeffs of the negative-degree terms
    for i in range(n + 1):  # {0, 1, ..., n}
        c[2 * i] = c_list[i] / d  # set the coeffs of the positive-degree terms

    return c


def step5(n, c_matrices, return_matrices=False):
    """
    Computes E(t)s from C(t)s by Qs and Ps
    :param n: the same n output by step 1
    :param c_matrices: a dictionary of the 2n+1 coefficient matrices from the FFT of step 4. dict keys are -2n,-2n+2,...,2n
    :return: a dictionary of projector matrices (each entry is a tuple of P and Q, except E0) or a dictionary of angles (default)
    """

    big_es = {}  # key=superscript of each primitive matrix, currently represented as (P, Q) tuple. Except E_0 = C_0
    all_cs = {2 * n: c_matrices}
    for m in range(2 * n, 0, -1):  # m = 2n, 2n-1, ... 2, 1
        # (part i)
        c_m = all_cs[m][m]
        q_m = c_m.H * c_m

        spec_norm = sqrt(max(chop(eig(q_m.H * q_m)[0])))  # default tolerance of mpmath.chop
        q_m = q_m / spec_norm  # normalizing
        p_m = eye(2) - q_m

        # E = tP + t^(-1)Q , but really only P is needed
        # the matrices E are just a tuple of P and Q, except Esub0 is a single matrix
        big_es[m] = (p_m, q_m)

        # (part ii)
        all_cs[m - 1] = {}  # adding nested dictionary to dictionary
        for k in range(-m + 1, m, 2):
            all_cs[m - 1][k] = matrix(all_cs[m][k - 1]) * p_m + matrix(
                    all_cs[m][k + 1]) * q_m  # eq (18)
            if m == 1 and k == 0:  # add this last one ( C_0^(0) )
                big_es[0] = all_cs[0][0]

    if return_matrices:
        return big_es
    else:
        angle_decomposition = {}
        for E in big_es.keys():
            if E != 0:
                # finds the primitive matrix E(m),
                # takes P from the tuple, takes the upper right element,
                # then finds the corresponding angle
                # this works because eq(10) becomes Pj = ([0.5, 0.5exp(i*phi_j)], [0.5exp(-i*phi_j), 0.5]) Eq(10)
                angle_decomposition[E] = polar(big_es[E][0][0, 1])[1]
                if angle_decomposition[E] < 0:
                    angle_decomposition[E] = angle_decomposition[E] + 2 * pi
            else:
                angle_decomposition[0] = 2 * polar(big_es[0][0, 0])[
                    1]  # the polar angle of the first element of C_0
        return angle_decomposition
