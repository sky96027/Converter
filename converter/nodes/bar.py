# converter/nodes/bar.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_BAR, LATEX_TO_HANGUL_BAR

class BarNode(ExprNode):
    """
    bar 기호 표현 노드
    ex) BarNode('bar', x) → \bar{x}
    """

    def __init__(self, op: str, arg: ExprNode):
        self.op = HANGUL_TO_LATEX_BAR.get(op, op)
        self.arg = arg

    def to_latex(self) -> str:
        return f"{self.op}{{{self.arg.to_latex()}}}"

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_BAR.get(self.op, self.op)
        return f"{hangul_op} {self.arg.to_hangul()}"

    def __repr__(self):
        return f"BarNode('{self.op}', {repr(self.arg)})"