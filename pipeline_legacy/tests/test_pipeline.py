# tests/test_pipeline.py

import unittest
from converter.pipeline.parse import parse_hangul_to_latex, parse_latex_to_hangul

def print_debug(expected, actual):
    if expected != actual:
        print("\n[DEBUG] 예상값:", repr(expected))
        print("[DEBUG] 실제값:", repr(actual))

class TestExpressionConversion(unittest.TestCase):

    # Power
    def test_power_latex_to_hangul(self):
        latex = "2 ^ 3"
        expected = "2 POWER 3"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_power_hangul_to_latex(self):
        hangul = "2 POWER 3"
        expected = "2 ^ 3"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # Log
    def test_log_latex_to_hangul(self):
        latex = r"\log_{2}{8}"
        expected = "LOG 2 8"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_log_hangul_to_latex(self):
        hangul = "LOG 2 8"
        expected = r"\log_{2}{8}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # Binom
    def test_binom_latex_to_hangul(self):
        latex = r"\binom{5}{2}"
        expected = "BINOM {5} {2}"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_binom_hangul_to_latex(self):
        hangul = "BINOM {5} {2}"
        expected = r"\binom{5}{2}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # Fraction
    def test_fraction_latex_to_hangul(self):
        latex = r"\frac{3}{4}"
        expected = "FRAC {3} {4}"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_fraction_hangul_to_latex(self):
        hangul = "FRAC {3} {4}"
        expected = r"\frac{3}{4}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # Integral
    def test_integral_latex_to_hangul(self):
        latex = r"\int_{0}^{1} x dx"
        expected = "INTEGRAL _{0}^{1} x dx"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_integral_hangul_to_latex(self):
        hangul = "INTEGRAL _{0}^{1} x dx"
        expected = r"\int_{0}^{1} x dx"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # Root
    def test_root_latex_to_hangul(self):
        latex = r"\sqrt[3]{5}"
        expected = "ROOT [3]{5}"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_root_hangul_to_latex(self):
        hangul = "ROOT [3]{5}"
        expected = r"\sqrt[3]{5}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - PLUS
    def test_plus_latex_to_hangul(self):
        latex = "1 + 2"
        expected = "1 PLUS 2"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_plus_hangul_to_latex(self):
        hangul = "1 PLUS 2"
        expected = "1 + 2"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - MINUS
    def test_minus_latex_to_hangul(self):
        latex = "5 - 3"
        expected = "5 MINUS 3"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_minus_hangul_to_latex(self):
        hangul = "5 MINUS 3"
        expected = "5 - 3"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - TIMES
    def test_times_latex_to_hangul(self):
        latex = r"4 \times 6"
        expected = "4 TIMES 6"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_times_hangul_to_latex(self):
        hangul = "4 TIMES 6"
        expected = r"4 \times 6"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - DIV
    def test_div_latex_to_hangul(self):
        latex = r"8 \div 2"
        expected = "8 DIV 2"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_div_hangul_to_latex(self):
        hangul = "8 DIV 2"
        expected = r"8 \div 2"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - EQUAL
    def test_equal_latex_to_hangul(self):
        latex = "x = y"
        expected = "x EQUAL y"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_equal_hangul_to_latex(self):
        hangul = "x EQUAL y"
        expected = "x = y"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - GREATER
    def test_greater_latex_to_hangul(self):
        latex = "5 > 2"
        expected = "5 GREATER 2"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_greater_hangul_to_latex(self):
        hangul = "5 GREATER 2"
        expected = "5 > 2"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - LESS
    def test_less_latex_to_hangul(self):
        latex = "3 < 9"
        expected = "3 LESS 9"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_less_hangul_to_latex(self):
        hangul = "3 LESS 9"
        expected = "3 < 9"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - GE
    def test_ge_latex_to_hangul(self):
        latex = r"7 \geq 4"
        expected = "7 GE 4"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_ge_hangul_to_latex(self):
        hangul = "7 GE 4"
        expected = r"7 \geq 4"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - LE
    def test_le_latex_to_hangul(self):
        latex = r"2 \leq 9"
        expected = "2 LE 9"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_le_hangul_to_latex(self):
        hangul = "2 LE 9"
        expected = r"2 \leq 9"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    # BinaryOp - NE
    def test_ne_latex_to_hangul(self):
        latex = r"a \neq b"
        expected = "a NE b"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_ne_hangul_to_latex(self):
        hangul = "a NE b"
        expected = r"a \neq b"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

        # Function - SIN

    def test_sin_latex_to_hangul(self):
        latex = r"\sin{x}"
        expected = "SIN x"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_sin_hangul_to_latex(self):
        hangul = "SIN x"
        expected = r"\sin{x}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

        # Function - COS

    def test_cos_latex_to_hangul(self):
        latex = r"\cos{y}"
        expected = "COS y"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_cos_hangul_to_latex(self):
        hangul = "COS y"
        expected = r"\cos{y}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

        # Function - TAN

    def test_tan_latex_to_hangul(self):
        latex = r"\tan{z}"
        expected = "TAN z"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_tan_hangul_to_latex(self):
        hangul = "TAN z"
        expected = r"\tan{z}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

        # Limit - 수정함

    def test_limit_latex_to_hangul(self):
        latex = r"\lim_{x \to 0} x"
        expected = "lim _{x \to 0} x"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_limit_hangul_to_latex(self):
        hangul = "lim _{x \to 0} x"
        expected = r"\lim_{x \to 0} x"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

        # Subscript

    def test_subscript_latex_to_hangul(self):
        latex = "A_{B}"
        expected = "SUB A B"
        actual = parse_latex_to_hangul(latex)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)

    def test_subscript_hangul_to_latex(self):
        hangul = "SUB A B"
        expected = "A_{B}"
        actual = parse_hangul_to_latex(hangul)
        print_debug(expected, actual)
        self.assertEqual(expected, actual)