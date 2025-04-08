# converter/nodes/root.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_ROOT, LATEX_TO_HANGUL_ROOT

class RootNode(ExprNode):
    """
    제곱근 수식 (sqrt 또는 \\sqrt)을 표현하는 노드
    - sqrt x → \\sqrt{x}
    - sqrt[n] of x → \\sqrt[n]{x}
    """

    def __init__(self, op, *args):
        self.op = HANGUL_TO_LATEX_ROOT.get(op, op)
        self.args = list(args)

    def to_latex(self) -> str:
        if len(self.args) == 1:
            radicand = self.args[0].to_latex()
            return f"{self.op}{{{radicand}}}"
        elif len(self.args) == 2:
            index = self.args[0].to_latex()
            radicand = self.args[1].to_latex()
            return f"{self.op}[{index}]{{{radicand}}}"
        return self.op

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_ROOT.get(self.op, self.op)
        if len(self.args) == 1:
            radicand = self.args[0].to_hangul()
            return f"{hangul_op} {{{radicand}}}"
        elif len(self.args) == 2:
            index = self.args[0].to_hangul()
            radicand = self.args[1].to_hangul()
            return f"{hangul_op} {{{index}}} of {{{radicand}}}"
        return hangul_op

    def __repr__(self):
        return f"RootNode('{self.op}', {', '.join(repr(a) for a in self.args)})"