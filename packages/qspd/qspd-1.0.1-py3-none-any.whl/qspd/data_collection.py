import argparse
import json
import logging
import os
import sys
from itertools import combinations
from math import ceil
# https://stackoverflow.com/a/25823885
from timeit import default_timer as timer
from typing import Iterable

from mpmath import mp, ln, nstr, mpf, arange, e, ldexp
from numpy import logspace, linspace

from qspd import jacobi_anger, step1, step2, step3, step4, step5
from qspd.json_encoding import DataEncoder
from qspd.tests import estimate_error


def collect_data(taus: Iterable = range(1, 6), errors=None, root_partitioner=None, big_ns=None):
    if errors is None:
        errors = [1e-4]
    if big_ns is None:
        big_ns = [None]
    if root_partitioner is None:
        def root_partitioner(big_r):
            num_real_roots = len(big_r)
            half_num_real_roots, remainder = divmod(num_real_roots, 2)
            combos = list(combinations(range(num_real_roots), half_num_real_roots))
            if remainder != 0:
                combos.extend(combinations(range(num_real_roots), half_num_real_roots + 1))
            for combo in combos:
                big_r_1_indices = set(combo)
                big_r_1 = [big_r[i] for i in combo]
                big_r_2 = [big_r[i] for i in range(num_real_roots) if i not in big_r_1_indices]
                yield big_r_1, big_r_2
    print("[")
    first = True
    for tau in taus:
        for error in errors:
            for forced_big_n in big_ns:
                for record in create_records(tau, error, root_partitioner, forced_big_n):
                    if not first:
                        print(",")
                    json.dump(record, sys.stdout, cls=DataEncoder)
                    sys.stdout.flush()
                    first = False
    print("\n]")


def create_records(tau, error, root_partitioner, forced_n):
    logger = logging.getLogger("datacollection")
    logger.info(f"error={nstr(error)} tau={nstr(tau)} N={nstr(forced_n)}")
    early_times = {}
    start = timer()
    big_a, big_b = jacobi_anger(tau, error, forced_n)
    big_n = max(big_a.degree, big_b.degree) if forced_n is None else forced_n
    early_times["step0"] = timer() - start

    epsilon = error / 15
    mp.dps = int(ceil((big_n / 3) * ln(big_n / epsilon)))

    start = timer()
    a, b, n = step1(big_a, big_b, epsilon, forced_n)
    early_times["step1"] = timer() - start

    start = timer()
    p, roots = step2(a, b, n)
    early_times["step2"] = timer() - start

    big_c = [r for r in roots if r.imag > 0 and abs(r) < 1]
    big_r = [r.real for r in roots if r.imag == 0 and abs(r) < 1]
    assert 4 * len(big_c) + 2 * len(big_r) == len(roots)

    for partition in root_partitioner(big_r):
        big_r_1, big_r_2 = partition
        times = dict(early_times)

        start = timer()
        f = step3(a, b, n, p, roots, big_r_1=big_r_1, big_r_2=big_r_2)
        times["step3"] = timer() - start

        start = timer()
        c_mat_dict = step4(f, n)
        times["step4"] = timer() - start

        start = timer()
        angles = step5(n, c_mat_dict)

        times["step5"] = timer() - start

        error = estimate_error(big_a, big_b, angles)

        times["total"] = sum(time for step, time in times.items() if step != "step0")

        record = {
            "tau": tau,
            "epsilon": epsilon,
            "bigA": big_a,
            "bigB": big_b,
            "bigN": big_n,
            "dps": mp.dps,
            "a": a,
            "b": b,
            "n": n,
            "roots": roots,
            "bigR1": big_r_1,
            "bigR2": big_r_2,
            "bigF": f,
            "bigCs": c_mat_dict,
            "angles": angles,
            "error": error,
            "times": times
        }
        yield record


def main():
    parser = argparse.ArgumentParser(description="Collect data for different values of tau")
    parser.add_argument("--filename", type=str, default=None, help="The name of the file to save, or leave blank to print to stdout")
    parser.add_argument("--tau", type=float, nargs="+", help="The value for tau or the range (default=linear) of tau expressed by --tau min max numpoints (np.linspace)")
    parser.add_argument("--log-tau", action="store_true", help="If set, tau arguments are interpreted as np.logspace arguments instead of np.linspace, --tau must have 3 args")
    parser.add_argument("--error", type=float, nargs="+", help="The value(s) of error, controlling precision, or a logarithmic (base 10) range of errors expressed by --error minexp maxexp numpoints")
    parser.add_argument("--n", type=str, nargs="+", help="The value of N=n or the linear range of n expressed by --n min max numpoints (np.linspace), uses minumum decomp if not set, uses minimum of biggest decomp for all iterations if set to auto")
    args = parser.parse_args()
    filename = args.filename
    old_out = sys.stdout
    if filename is not None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        sys.stdout = open(filename, mode="w")
    logger = logging.getLogger("datacollection")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    def root_partitioner(big_r):
        num_real_roots = len(big_r)
        half_num_real_roots, remainder = divmod(num_real_roots, 2)
        combos = list(combinations(range(num_real_roots), half_num_real_roots))
        num_combos = len(combos)
        assert num_combos > 0
        if num_combos <= 1:
            combo = combos[0]
        else:
            combo = max(combos, key=lambda c: sum(big_r[i] for i in c))
            if num_combos > 2:
                logger.warning(f"Lots of combos: {combos}")
        big_r_1_indices = set(combo)
        big_r_1 = [big_r[i] for i in combo]
        big_r_2 = [big_r[i] for i in range(num_real_roots) if i not in big_r_1_indices]
        yield big_r_1, big_r_2

    tau = args.tau
    if tau is None:
        taus = [10]
    elif len(tau) == 1:
        taus = tau
    elif len(tau) == 3:
        if args.log_tau:
            taus = logspace(tau[0], tau[1], int(tau[2]))
        else:
            taus = linspace(tau[0], tau[1], int(tau[2]))
    else:
        raise AssertionError("--tau should have 1 (ex: 80), or 3 (ex: 10 20 5) (np.linspace) arguments")
    min_str = nstr(min(taus))
    max_str = nstr(max(taus))
    if args.log_tau and len(taus) == 3:
        min_str = "10^" + min_str
        max_str = "10^" + max_str

    error = args.error
    if error is None:
        errors = [0.001]
    elif len(error) == 1:
        errors = error
    elif len(error) == 3:
        errors = logspace(error[0], error[1], error[2])
    else:
        raise AssertionError("--error should have 1 (ex: .000001), or 3 (np.logspace, ex: -4 -9 4) arguments")

    n = args.n
    if n is None:
        ns = n
    elif n == ["auto"]:
        ns = [int(ceil(ldexp(e, -1) * max(taus) - ln(min(errors))))]
    elif len(n) == 1:
        ns = [int(n[0])]
    elif len(n) == 3:
        ns = [int(round(i)) for i in linspace(*list(map(int, n)))]
    else:
        raise AssertionError("--n should have 1 (ex: 145), or 3 (ex: 30, 36, 1) (np.linspace) integer arguments")

    if n is None:
        logger.info(f"Running {len(taus)} iteration(s) from tau={min_str} to tau={max_str}, {len(errors)} iteration(s) from error={min(errors)} to error={max(errors)}, and N=n is not forced larger than needed ")
    else:
        logger.info(f"Running {len(taus)} iteration(s) from tau={min_str} to tau={max_str}, {len(errors)} iteration(s) from error={min(errors)} to error={max(errors)}, and {len(ns)} iteration(s) from N=n={min(ns)} to N=n={max(ns)} ")
    collect_data(taus=taus, errors=errors, root_partitioner=root_partitioner, big_ns=ns)

    if filename is not None:
        sys.stdout.close()
        sys.stdout = old_out


if __name__ == '__main__':
    main()
