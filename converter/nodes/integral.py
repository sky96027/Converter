# converter/nodes/integral.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_INTEGRAL, LATEX_TO_HANGUL_INTEGRAL

class IntegralNode(ExprNode):
    """
    정적분 표현 노드 (예: \int_{a}^{b} f(x) dx)
    """

    def __init__(self, op, *args):
        if op in HANGUL_TO_LATEX_INTEGRAL:
            self.op = HANGUL_TO_LATEX_INTEGRAL[op]
        else:
            self.op = op
        self.args = list(args)

    def to_latex(self) -> str:
        if len(self.args) == 4:
            lower = self.args[0].to_latex()
            upper = self.args[1].to_latex()
            body = self.args[2].to_latex()
            dx = self.args[3].to_latex()
            return f"{self.op}_{{{lower}}}^{{{upper}}} {body} \\, {dx}"
        return self.op

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_INTEGRAL.get(self.op, self.op)
        if len(self.args) == 4:
            lower = self.args[0].to_hangul()
            upper = self.args[1].to_hangul()
            body = self.args[2].to_hangul()
            dx = self.args[3].to_hangul()
            return f"{hangul_op}_ {{{lower}}} ^ {{{upper}}} {body} {dx}"
        return hangul_op

    def __repr__(self):
        return f"IntegralNode('{self.op}', {', '.join(repr(a) for a in self.args)})"

