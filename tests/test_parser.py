# tests/test_parser.py

import unittest
from converter import parse_hangul, parse_latex

class GeneratedOperatorTests(unittest.TestCase):
    def assert_formula_debug(self, expected, actual, expr=None, ast=None, always_print=False):
        print("\n=== 디버깅 정보 ===")
        if expr is not None:
            print("수식:", expr)
            if '\\' in expr:
                print("변환 방향: LATEX → HANGUL")
            else:
                print("변환 방향: HANGUL → LATEX")
        if ast is not None:
            print("AST 구조 (repr):", repr(ast))
        print(f"예상값: {repr(expected)}")
        print(f"실제값: {repr(actual)}")
        print("================")
        self.assertEqual(expected, actual)

    # FunctionNode: LaTeX → 한글 ( sin, 중첩 괄호, 공백 Edge Case )
    def test_function_node_hangul_to_latex_nested_expr(self):
        # 함수 인자에 괄호가 포함된 복합 수식 (한글 → LaTeX)
        expr = "sin {x + (y +1 )}"
        expected = r"\sin{x + ( y + 1 )}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FunctionNode: LaTeX → 한글 ( sin, 중첩 괄호, 공백 Edge Case )
    def test_function_node_latex_to_hangul_nested_expr(self):
        # 함수 인자에 괄호가 포함된 복합 수식 (LaTeX → 한글)
        expr = r"\sin{x + (            y+         1)}"
        expected = "sin {x + ( y + 1 )}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FunctionNode: 한글 → LaTeX (cos)
    def test_function_node_hangul_to_latex_cos(self):
        expr = "cos {x}"
        expected = r"\cos{x}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FunctionNode: LaTeX → 한글 (cos)
    def test_function_node_latex_to_hangul_cos(self):
        expr = r"\cos{x}"
        expected = "cos {x}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FunctionNode: 한글 → LaTeX (tan)
    def test_function_node_hangul_to_latex_tan(self):
        expr = "tan {x}"
        expected = r"\tan{x}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FunctionNode: LaTeX → 한글 (tan)
    def test_function_node_latex_to_hangul_tan(self):
        expr = r"\tan{x}"
        expected = "tan {x}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # RootNode: 한글 → LaTeX (with 'of')
    def test_root_node_hangul_to_latex(self):
        expr = "sqrt {3} of {x + 1}"
        expected = r"\sqrt[3]{x + 1}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # RootNode: LaTeX → 한글 (with 'of')
    def test_root_node_latex_to_hangul(self):
        expr = r"\sqrt[3]{x + 1}"
        expected = "sqrt {3} of {x + 1}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # LogNode: 한글 → LaTeX
    def test_log_node_hangul_to_latex(self):
        expr = "log {x + 1}"
        expected = r"\log{x + 1}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # LogNode: LaTeX → 한글
    def test_log_node_latex_to_hangul(self):
        expr = r"\log{x + 1}"
        expected = "log {x + 1}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FractionNode: 한글 → LaTeX
    def test_fraction_node_hangul_to_latex(self):
        expr = "1 over {x + 1}"
        expected = r"\frac{1}{x + 1}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # FractionNode: LaTeX → 한글
    def test_fraction_node_latex_to_hangul(self):
        expr = r"\frac{1}{x + 1}"
        expected = "1 over {x + 1}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast, always_print=True)

    # PowerNode: 한글 → LaTeX
    def test_power_node_hangul_to_latex(self):
        expr = "x ^ {2}"
        expected = r"x^{2}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast)

    # PowerNode: LaTeX → 한글
    def test_power_node_latex_to_hangul(self):
        expr = r"x^{2}"
        expected = "x ^ {2}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast)

    # # IntegralNode: 한글 → LaTeX ( 복잡한 수식 )
    # def test_integral_node_hangul_to_latex_complicated(self):
    #     expr = "int _{-2} ^{0} f ( x ) dx = int _{-2} ^{0} f ( x ) dx"
    #     expected = r"\int_{-2}^{0} f(x) \, dx = \int_{-2}^{0} f(x) \, dx"
    #     ast = parse_hangul(expr)
    #     actual = ast.to_latex()
    #     print("▶ ast.to_latex():", ast.to_latex())
    #     self.assert_formula_debug(expected, actual, expr=expr, ast=ast)

    # IntegralNode: LaTeX → 한글 ( 간단한 수식 )
    def test_integral_node_latex_to_hangul_simple(self):
        expr = r"\int_{-2}^{0} f ( x ) \, dx"
        expected = "int_ {-2} ^ {0} f ( x ) dx"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast)

    # CaseNode: 한글 -> LaTeX
    def test_cases_node_hangul_to_latex(self):
        expr = "cases {x && x > 0 # -x && x <= 0}"
        expected = r"\begin{cases} x & x > 0 \\ -x & x <= 0 \end{cases}"
        ast = parse_hangul(expr)
        actual = ast.to_latex()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast)

    # CaseNode: LaTeX -> 한글
    def test_cases_node_latex_to_hangul(self):
        expr = r"\begin{cases} x & x > 0 \\ -x & x <= 0 \end{cases}"
        expected = "cases {x && x > 0 # -x && x <= 0}"
        ast = parse_latex(expr)
        actual = ast.to_hangul()
        self.assert_formula_debug(expected, actual, expr=expr, ast=ast)




