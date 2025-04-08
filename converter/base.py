# converter/base.py

from abc import ABC, abstractmethod

class ExprNode(ABC):
    """모든 수식 노드의 추상 기반 클래스"""

    @abstractmethod
    def to_latex(self) -> str:
        """LaTeX 수식 문자열로 변환"""
        pass

    @abstractmethod
    def to_hangul(self) -> str:
        """한글 수식 문자열로 변환"""
        pass

    def __str__ (self) -> str:
        return f"<{self.__class__.__name__}: {self.to_latex()}>"
