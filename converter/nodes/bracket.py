# converter/nodes/bracket.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_BRACKET, LATEX_TO_HANGUL_BRACKET

class BracketNode(ExprNode):
    """
    괄호 표현 노드
    ex) BracketNode('left', '(', inner, ')', 'right')
    """

    def __init__(self, left_tag: str, lparen: str, content: ExprNode, rparen: str, right_tag: str):
        self.left_tag = left_tag   # ex) 'left' or '\\left'
        self.lparen = lparen       # ex) '(', '[', etc.
        self.inner = content       # AST
        self.rparen = rparen
        self.right_tag = right_tag

    def to_latex(self) -> str:
        left_tag = r"\left" if self.left_tag.casefold() in ["left", "\\left"] else self.left_tag
        right_tag = r"\right" if self.right_tag.casefold() in ["right", "\\right"] else self.right_tag
        inner = self.inner.to_latex()
        return f"{left_tag}{self.lparen}{inner}{right_tag}{self.rparen}"

    def to_hangul(self) -> str:
        left_tag = "left" if self.left_tag.casefold() in ["left", "\\left"] else self.left_tag
        right_tag = "right" if self.right_tag.casefold() in ["right", "\\right"] else self.right_tag
        inner = self.inner.to_hangul()
        return f"{left_tag}{self.lparen}{inner}{right_tag}{self.rparen}"

    def __repr__(self):
        return f"BracketNode('{self.left_tag}', '{self.lparen}', {repr(self.inner)}, '{self.rparen}', '{self.right_tag}')"