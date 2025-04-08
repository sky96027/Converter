# converter/nodes/matrix.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_MATRIX, LATEX_TO_HANGUL_MATRIX

class MatrixNode(ExprNode):
    """
    행렬 표현 노드 (예: \begin{matrix} ... \end{matrix})
    """

    def __init__(self, op, *args):
        if op in HANGUL_TO_LATEX_MATRIX:
            self.op = HANGUL_TO_LATEX_MATRIX[op]
        else:
            self.op = op
        self.args = list(args)  # 각 row는 LiteralNode("1 & 2") 형태로 들어옴

    def to_latex(self) -> str:
        content = r" \\\\ ".join(arg.to_latex() for arg in self.args)
        return f"\\begin{{matrix}} {content} \\end{{matrix}}"

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_MATRIX.get(self.op, self.op)
        content = " # ".join(arg.to_hangul() for arg in self.args)
        return f"{hangul_op} {content}"

    def __repr__(self):
        return f"MatrixNode('{self.op}', {', '.join(repr(a) for a in self.args)})"