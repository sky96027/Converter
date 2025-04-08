# converter/nodes/power.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_POWER, LATEX_TO_HANGUL_POWER

class PowerNode(ExprNode):
    """
    거듭제곱 표현 노드 (예: x^{2})
    """

    def __init__(self, op, *args):
        self.op = HANGUL_TO_LATEX_POWER.get(op, op)
        self.args = list(args)

    def to_latex(self) -> str:
        if len(self.args) == 2:
            base = self.args[0].to_latex()
            exponent = self.args[1].to_latex()
            return f"{base}{self.op}{{{exponent}}}"
        return self.op

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_POWER.get(self.op, self.op)
        if len(self.args) == 2:
            base = self.args[0].to_hangul()
            exponent = self.args[1].to_hangul()
            return f"{base} {hangul_op} {{{exponent}}}"
        return hangul_op

    def __repr__(self):
        return f"PowerNode('{self.op}', {', '.join(repr(a) for a in self.args)})"