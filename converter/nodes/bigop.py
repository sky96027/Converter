# converter/nodes/bigop.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_BIGOP, LATEX_TO_HANGUL_BIGOP

class BigOpNode(ExprNode):
    """
    누산 기호 노드 (SIGMA, PI 등) - 예: \sum_{i=1}^{n} i
    """

    def __init__(self, op, *args):
        if op in HANGUL_TO_LATEX_BIGOP:
            self.op = HANGUL_TO_LATEX_BIGOP[op]
        else:
            self.op = op
        self.args = list(args)

    def to_latex(self) -> str:
        if len(self.args) == 3:
            lower = self.args[0].to_latex()
            upper = self.args[1].to_latex()
            expr = self.args[2].to_latex()
            return f"{self.op}_{{{lower}}}^{{{upper}}} {expr}"
        return f"{self.op} " + " ".join(arg.to_latex() for arg in self.args)

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_BIGOP.get(self.op, self.op)
        return f"{hangul_op} " + " ".join(arg.to_hangul() for arg in self.args)

    def __repr__(self):
        return f"BigOpNode('{self.op}', {', '.join(repr(a) for a in self.args)})"