# converter/nodes/binary_op.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_BINARY_OP, LATEX_TO_HANGUL_BINARY_OP

class BinaryOpNode(ExprNode):
    """모든 이항 연산을 담당하는 핵심 노드"""

    def __init__(self, op, left, right):
        self.op = op.strip()
        self.left = left
        self.right = right

    def to_latex(self) -> str:
        left_str = self.left.to_latex()
        right_str = self.right.to_latex()

        latex_op = HANGUL_TO_LATEX_BINARY_OP.get(self.op, self.op)
        return f"{left_str} {latex_op} {right_str}"

    def to_hangul(self) -> str:
        left_str = self.left.to_hangul()
        right_str = self.right.to_hangul()

        hangul_op = LATEX_TO_HANGUL_BINARY_OP.get(self.op, self.op)

        print("[DEBUG to_hangul] (LaTeX → HANGUL 변환)")
        print(f"  self.op         = '{self.op}'")
        print(f"  hangul_op       = '{hangul_op}'")
        print(f"  final_str       = '{left_str} {hangul_op} {right_str}'")

        return f"{left_str} {hangul_op} {right_str}"

    def __repr__(self):
        return f"BinaryOpNode('{self.op}', {repr(self.left)}, {repr(self.right)})"