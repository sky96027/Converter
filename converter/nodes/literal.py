# converter/nodes/literal.py
from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_SYMBOL, LATEX_TO_HANGUL_SYMBOL


class LiteralNode(ExprNode):
    """
    단순한 숫자, 문자, 기호 등을 나타내는 Literal 노드
    ex ) '1', 'x''
    """

    def __init__(self, value: str):
        self.value = value

    def to_latex(self) -> str:
        return self.value

    def to_hangul(self) -> str:
        return self.value
        
    def __repr__(self):
        return f"LiteralNode('{self.value}')"


