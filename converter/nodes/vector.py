# converter/nodes/vector.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_VECTOR, LATEX_TO_HANGUL_VECTOR

class VectorNode(ExprNode):
    """
    벡터 또는 단위벡터를 나타내는 노드
    ex) \vec{v}, \hat{i}
    """

    def __init__(self, op, arg):
        self.op = HANGUL_TO_LATEX_VECTOR.get(op, op)
        self.arg = arg

    def to_latex(self) -> str:
        return f"{self.op}{{{self.arg.to_latex()}}}"

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_VECTOR.get(self.op, self.op)
        return f"{hangul_op} {self.arg.to_hangul()}"

    def __repr__(self):
        return f"VectorNode('{self.op}', {repr(self.arg)})"