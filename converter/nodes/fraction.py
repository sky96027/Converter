# converter/nodes/fraction.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_FRACTION, LATEX_TO_HANGUL_FRACTION


class FractionNode(ExprNode):
    """
    분수 표현 노드 (예: \\frac{a}{b})
    ex ) \frac{1}{2} ↔ 1 over {2}
    """

    def __init__(self, op, *args):
        if op in HANGUL_TO_LATEX_FRACTION:
            self.op = HANGUL_TO_LATEX_FRACTION[op]
        else:
            self.op = op
        self.args = list(args)

    def to_latex(self) -> str:
        latex_op = HANGUL_TO_LATEX_FRACTION.get(self.op, self.op)
        if len(self.args) == 2:
            numerator = self.args[0].to_latex()
            denominator = self.args[1].to_latex()
            return f"{latex_op}{{{numerator}}}{{{denominator}}}"
        return latex_op

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_FRACTION.get(self.op, self.op)
        if len(self.args) == 2:
            numerator = self.args[0].to_hangul()
            denominator = self.args[1].to_hangul()
            return f"{numerator} {hangul_op} {{{denominator}}}"
        return hangul_op

    def __repr__(self):
        return f"FractionNode('{self.op}', {', '.join(repr(a) for a in self.args)})"