from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_FUNCTION, LATEX_TO_HANGUL_FUNCTION


class FunctionNode(ExprNode):
    """
    일반 함수 표현 노드 (예: sin, cos, tan 등)
    ex ) \sin{x + 1} ↔ sin {x + 1}
    """

    def __init__(self, op, *args):
        # 항상 self.op은 LaTeX 기준으로 저장
        self.op = HANGUL_TO_LATEX_FUNCTION.get(op, op)
        self.args = list(args)

    def to_latex(self) -> str:
        """
        함수 → LaTeX 변환
        - 함수명: self.op
        - 인자: 항상 중괄호로 감쌈
        """
        args_str = " ".join(arg.to_latex() for arg in self.args)
        return f"{self.op}{{{args_str}}}"

    def to_hangul(self) -> str:
        """
        함수 → 한글 변환
        - 함수명: 한글로 치환
        - 인자: 중괄호 유지
        """
        op_hangul = LATEX_TO_HANGUL_FUNCTION.get(self.op, self.op)
        args_str = " ".join(f"{{{arg.to_hangul()}}}" for arg in self.args)
        return f"{op_hangul} {args_str}"

    def __repr__(self):
        return f"FunctionNode('{self.op}', {', '.join(repr(a) for a in self.args)})"