# converter/nodes/symbol.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_SYMBOL, LATEX_TO_HANGUL_SYMBOL

class SymbolNode(ExprNode):
    def __init__(self, op: str):
        self.op = HANGUL_TO_LATEX_SYMBOL.get(op, op)

    def to_latex(self) -> str:
        return self.op

    def to_hangul(self) -> str:
        return LATEX_TO_HANGUL_SYMBOL.get(self.op, self.op)

    def __repr__(self):
        return f"SymbolNode('{self.op}')"