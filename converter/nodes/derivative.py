# converter/nodes/derivative.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_DERIV, LATEX_TO_HANGUL_DERIV

class DerivativeNode(ExprNode):
    """
    도함수(미분) 표현: f', f'', 등
    """

    def __init__(self, op, func):
        self.op = HANGUL_TO_LATEX_DERIV.get(op, op)
        self.func = func

    def to_latex(self) -> str:
        return f"{self.func.to_latex()}{self.op}"

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_DERIV.get(self.op, self.op)
        return f"{self.func.to_hangul()} {hangul_op}"

    def __repr__(self):
        return f"DerivativeNode('{self.op}', {repr(self.func)})"