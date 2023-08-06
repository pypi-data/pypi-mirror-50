from fractions import Fraction
from json import JSONEncoder
from numbers import Rational

from mpmath import mpf, mpc, matrix
from sympy import Matrix

from qspd.util import InputFunction, Parity, ImaginaryRational


class DataEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, InputFunction):
            return {"parity": o.parity, "coeffs": {k: o[k] for k in o}}
        if isinstance(o, Parity):
            if o == Parity.EVEN:
                return "even"
            else:
                assert o == Parity.ODD
                return "odd"
        if isinstance(o, (mpf, mpc)):
            return repr(o)
        if isinstance(o, Fraction):
            return {"numerator": o.numerator, "denominator": o.denominator, "imaginary": False}
        if isinstance(o, ImaginaryRational):
            return {"numerator": o.numerator, "denominator": o.denominator, "imaginary": True}
        if isinstance(o, Matrix):
            return matrix(o)
        if isinstance(o, matrix):
            return o.tolist()
        return JSONEncoder.default(self, o)


def decode_data(data_list):
    def decode_record(record):
        record["tau"] = decode_float(record["tau"]) if "tau" in record else None
        record["epsilon"] = decode_float(record["epsilon"]) if "epsilon" in record else None
        record["bigA"] = decode_input_function(record["bigA"]) if "bigA" in record else None
        record["bigB"] = decode_input_function(record["bigB"]) if "bigB" in record else None
        record["bigN"] = int(record["bigN"]) if "bigN" in record else None
        record["dps"] = int(record["dps"]) if "dps" in record else None
        record["a"] = decode_rational_function(record["a"]) if "a" in record else None
        record["b"] = decode_rational_function(record["b"]) if "b" in record else None
        record["n"] = decode_n(record)
        record["roots"] = [decode_float(v) for v in record["roots"]] if "roots" in record else None
        record["bigR1"] = decode_float_list(record["bigR1"]) if "bigR1" in record else None
        record["bigR2"] = decode_float_list(record["bigR2"]) if "bigR2" in record else None
        record["bigF"] = [Matrix(2, 2, list(decode_matrix(v))) for v in
                          record["bigF"]] if "bigF" in record else None
        record["bigCs"] = {k: decode_matrix(v) for k, v in
                           record["bigCs"].items()} if "bigCs" in record else None
        record["angles"] = decode_angle_list(record["angles"]) if "angles" in record else None
        if "epsilonError" in record:
            # for the purpose of reading our old JSONs, (The error would be ~5 bc its in terms of epsilons)
            record["error"] = decode_float(record["epsilonError"]) / record["epsilon"]
        elif "error" in record:
            # New data JSONs should have error only (not in terms of epsilons)
            record["error"] = decode_float(record["error"])
        else:
            record["error"] = None
        if "times" in record and isinstance(record["times"], float):
            record["times"] = {"total": record["times"]}
        return record

    def decode_float(value):
        if isinstance(value, str):
            try:
                return mpf(value)
            except ValueError:
                return eval(value)
        return value

    def decode_input_function(obj):
        parity = decode_parity(obj["parity"])
        coeffs = {int(k): decode_float(v) for k, v in obj["coeffs"].items()}
        return InputFunction(coeffs, parity)

    def decode_parity(obj):
        if obj == "even":
            return Parity.EVEN
        else:
            assert obj == "odd"
            return Parity.ODD

    def decode_rational_function(obj):
        return {k: decode_rational(v) for k, v in obj.items()}

    def decode_rational(obj):
        if isinstance(obj, (Rational, ImaginaryRational)):
            return obj
        numerator = int(obj["numerator"])
        denominator = int(obj["denominator"])
        imaginary = bool(obj["imaginary"])
        if imaginary:
            return ImaginaryRational(numerator, denominator)
        else:
            return Fraction(numerator, denominator)

    def decode_float_list(obj):
        return [decode_float(v) for v in obj]

    def decode_matrix(obj):
        floats = [[decode_float(value) for value in row] for row in obj]
        return matrix(floats)

    def decode_angle_list(obj):
        if isinstance(obj, dict):
            return [decode_float(obj[str(i)]) for i in range(len(obj))]
        elif isinstance(obj, list):
            return [decode_float(angle) for angle in obj]

    def decode_n(record):
        if "n" in record:
            return int(record["n"])
        if "angles" in record:
            return len(record["angles"]) // 2
        return None

    return [decode_record(record) for record in data_list]
