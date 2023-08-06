from collections import defaultdict

from mpmath import expj, matrix, eye, zeros, chop, mpc, pi, mpf, j, expjpi, workdps

from qspd import InputFunction, Parity
from qspd.util import polyval_dict


def estimate_error(big_a, big_b, angles, num_points=None):
    """
    Calculates the closeness between the input function A+Bi and the estimated version A'+B'i.
    We input values from the unit circle into both functions and compare the difference in outputs.
    The number of evenly spaced points is 5 times the polynomial degree

    :param big_a: Dictionary of coefficients of original A
    :param big_b: Dictionary of coefficients of original B
    :param angles: used to recompose the the A' + B' i
    :return: the maximum difference between the original A+iB and the resulting A'+B'i
    """
    num_points = int(5*(len(angles)-1)/2)
    max_error = 0
    output_big_a, output_big_b = recompose(angles)
    for k in range(num_points):
        z = expjpi(2*mpf(k)/mpf(num_points))
        expected = polyval_dict(big_a, z) + j*polyval_dict(big_b, z)
        calculated = polyval_dict(output_big_a, z) + j*polyval_dict(output_big_b, z)
        max_error = max(max_error, abs(expected-calculated))
    return max_error


def recompose(angles):
    """
    Reverses the matrix decomposition performed by steps 1-5:
    Given the angles output by step5(), this function computes A(z) and B(z), the inputs to step1().
    :param angles: (list of mpf's) the 2n+1 angles computed by step5().
                    Each angle[j] corresponds to a matrix E_j in equation 19.
                    len(angles) must be odd
    :return: The functions A(z) and B(z), as FloatFunctions,
            and the degree, big_n, of the functions
    """

    big_n, remainder = divmod(len(angles),
                              2)  # big_n is the degree of the polynomial we will compute
    if remainder == 0:  # there should be 2*big_n + 1 angles
        raise ValueError('angles must have an odd number of elements')

    # Step 1: Compute the matrix E0, corresponding to angle[0]
    e_0 = matrix([[expj(angles[0] / 2), 0],
                  [0, expj(-angles[0] / 2)]])  # the matrix E_0, defined in Haah section 3

    identity = eye(2)  # 2 x 2 identity matrix
    zero = zeros(2)  # 2 x 2 matrix of zeros

    prod = defaultdict(lambda: zero)  # the product E_0 * E_1 * E_2 * ... * E_{max_k}
    prod[0] = e_0

    # Step 2: Compute prod, the product of the E-matrices
    for k in range(1, len(angles)):  # omit angles[0]
        p_k = matrix([[1, expj(angles[k])],
                      [expj(-angles[k]), 1]]) / 2  # The projector matrix P corresponding to E_k
        q_k = identity - p_k  # The other projector Q corresponding to E_k

        # Each E_k_dagger = (P_k * t + Q_k * t^-1)^dagger is a binomial. Now expand the binomials into one polynomial.
        updated_prod = defaultdict(lambda: zero)
        for j, coeff in prod.items():
            updated_prod[j + 1] += coeff * q_k.H
            updated_prod[j - 1] += coeff * p_k.H
        prod = updated_prod  # the coefficients of prod are indexed by their t-degree, not z-degree

    # Step 3: Decompose each matrix in prod into real (A) and imaginary (B) matrices
    a = defaultdict(lambda: 0)  # the coeffs of the polynomial A(z)
    b = defaultdict(lambda: 0)  # the coeffs of the polynomial B(Z)

    def sum_div_2(mat):
        """
        :param mat: a 2x2 matrix
        :return: the sum of the four elements of the matrix, divided by 2
        This is equivalent to: <+|mat|+>
        """
        return (mat[0, 0] + mat[0, 1] + mat[1, 0] + mat[1, 1]) / 2

    for j in range(big_n + 1):
        # Note: We use prod[2 * j] to compute a[j], b[j] because a and b are indexed by z-degree,
        #       whereas prod uses t-degree
        f_j = sum_div_2(prod[2 * j])  # the coeff. of the jth term in <+|F(z)|+>
        f_mj = sum_div_2(prod[-2 * j])  # the coeff. of the -jth term in <+|F(z)|+>

        # Split the function <+|F(z)|+> into reciprocal A(Z) and anti-reciprocal B(Z) functions.
        recip = chop((f_j + f_mj) / 2)
        anti_recip = chop((f_j - f_mj) / mpc(0, 2))

        a[j] = recip
        a[-j] = recip
        b[j] = anti_recip
        b[-j] = -anti_recip

    # Update big_n in case the leading terms of a and b are zero
    big_n = max(j for j in range(big_n + 1) if a[j] != 0 or b[j] != 0)

    # Step 4: Convert a and b to FloatFunctions
    return InputFunction(a, Parity.EVEN, big_n), InputFunction(b, Parity.ODD, big_n)
