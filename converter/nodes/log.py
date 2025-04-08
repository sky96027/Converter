# converter/nodes/log.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_LOG, LATEX_TO_HANGUL_LOG

class LogNode(ExprNode):
    """
    로그 기호 (LOG 또는 \log)를 표현하는 노드.

    - 이 노드는 로그 기호 자체만 나타냄.
    """

    def __init__(self, op, *args):
        if op in HANGUL_TO_LATEX_LOG:
            self.op = HANGUL_TO_LATEX_LOG[op]
        else:
            self.op = op
        self.args = list(args)

    def to_latex(self) -> str:
        latex_op = self.op
        if len(self.args) == 2:
            base_str = self.args[0].to_latex()
            value_str = self.args[1].to_latex()
            return f"{latex_op}_{{{base_str}}}{{{value_str}}}"
        elif len(self.args) == 1:
            return f"{latex_op}{{{self.args[0].to_latex()}}}"
        else:
            return latex_op

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_LOG.get(self.op, self.op)
        if len(self.args) == 2:
            return f"{hangul_op}_{{{self.args[0].to_hangul()}}}{{{self.args[1].to_hangul()}}}"
        elif len(self.args) == 1:
            return f"{hangul_op} {{{self.args[0].to_hangul()}}}"
        return hangul_op

    def __repr__(self):
        return f"LogNode('{self.op}', {', '.join(repr(a) for a in self.args)})"