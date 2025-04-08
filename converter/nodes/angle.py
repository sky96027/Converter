# converter/nodes/angle.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_ANGLE, LATEX_TO_HANGUL_ANGLE

class AngleNode(ExprNode):
    """
    각도 표현 노드
    ex) AngleNode('angle', ABC) → \angle{ABC}
    xml에는 괄호를 사용하지 않지만 통일화를 위해 xml 파싱 단계에서 angle ABC -> angle {ABC} 로 바꿔줌
    """

    def __init__(self, op: str, arg: ExprNode):
        self.op = HANGUL_TO_LATEX_ANGLE.get(op, op)
        self.arg = arg

    def to_latex(self) -> str:
        return f"{self.op}{{{self.arg.to_latex()}}}"

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_ANGLE.get(self.op, self.op)
        return f"{hangul_op} {self.arg.to_hangul()}"

    def __repr__(self):
        return f"AngleNode('{self.op}', {repr(self.arg)})"