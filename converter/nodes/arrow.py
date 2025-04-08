# converter/nodes/arrow.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_ARROW, LATEX_TO_HANGUL_ARROW

class ArrowNode(ExprNode):
    """
    화살표 기호 (→, ←, ↦ 등)를 나타내는 노드
    ex ) a → b, x ← y, f ↦ g
    """

    def __init__(self, op, left, right):
        self.op = HANGUL_TO_LATEX_ARROW.get(op, op) if op in HANGUL_TO_LATEX_ARROW else op
        self.left = left
        self.right = right

    def to_latex(self) -> str:
        return f"{self.left.to_latex()} {self.op} {self.right.to_latex()}"

    def to_hangul(self) -> str:
        op = LATEX_TO_HANGUL_ARROW.get(self.op, self.op)
        return f"{self.left.to_hangul()} {op} {self.right.to_hangul()}"

    def __repr__(self):
        return f"ArrowNode('{self.op}', {repr(self.left)}, {repr(self.right)})"