# converter/nodes/limit.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_LIMIT, LATEX_TO_HANGUL_LIMIT

class LimitNode(ExprNode):
    """
    극한 표현 노드 (예: \lim_{x \\to 0} f(x))
    """

    def __init__(self, op, *args):
        if op in HANGUL_TO_LATEX_LIMIT:
            self.op = HANGUL_TO_LATEX_LIMIT[op]
        else:
            self.op = op
        self.args = list(args)

    def to_latex(self) -> str:
        if len(self.args) == 2:
            under = self.args[0].to_latex()
            body = self.args[1].to_latex()
            return f"{self.op}_{{{under}}} {body}"
        return self.op

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_LIMIT.get(self.op, self.op)
        if len(self.args) == 2:
            under = self.args[0].to_hangul()
            body = self.args[1].to_hangul()
            return f"{hangul_op} {{{under}}} {body}"
        return hangul_op

    def __repr__(self):
        return f"LimitNode('{self.op}', {', '.join(repr(a) for a in self.args)})"