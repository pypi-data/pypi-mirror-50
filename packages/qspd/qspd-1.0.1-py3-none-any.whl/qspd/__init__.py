from mpmath import ceil, ln, mp, ldexp, besselj, fmul, mpc, fneg, e, workdps

from qspd.steps import step1, step2, step3, step4, step5
from qspd.util import InputFunction, Parity

name = "qspd"


def qspd(big_a, big_b, error=1e-4, forced_n=None, return_matrices=False):
    epsilon = error / 15
    big_n = max(big_a.degree, big_b.degree) if forced_n is None else forced_n
    mp.dps = int(ceil((big_n / 3) * ln(big_n / epsilon)))
    a, b, n = step1(big_a, big_b, epsilon, forced_n)
    if forced_n is not None:
        n = forced_n
    p, roots = step2(a, b, n)
    big_f = step3(a, b, n, p, roots)
    c_matrices = step4(big_f, n)
    return step5(n, c_matrices, return_matrices)


def jacobi_anger(tau, error, forced_big_n=None):
    epsilon = error / 15
    if forced_big_n is None:
        big_n = int(ceil(ldexp(e, -1) * tau - ln(epsilon)))  # equation 38
    else:
        big_n = forced_big_n
    with workdps(int(ceil((big_n / 3) * ln(big_n / epsilon)))):
        a_coefficients = {}
        b_coefficients = {}
        for k in range(0, big_n + 1, 2):
            coefficient = besselj(k, tau)
            a_coefficients[k] = coefficient
            a_coefficients[-k] = coefficient
        for k in range(1, big_n + 1, 2):
            coefficient = fmul(besselj(k, tau), mpc(0, -1), exact=True)
            b_coefficients[k] = coefficient
            b_coefficients[-k] = fneg(coefficient, exact=True)
        big_a = InputFunction(a_coefficients, Parity.EVEN, big_n)
        big_b = InputFunction(b_coefficients, Parity.ODD, big_n)
        return big_a, big_b
