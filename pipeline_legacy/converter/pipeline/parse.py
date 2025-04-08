# converter/pipeline/parse.py

from converter.pipeline.tokenize import tokenize
from converter.pipeline.render import (
    render_hangul_to_latex,
    render_latex_to_hangul,
)


def parse_hangul_to_latex(expr: str) -> str:
    """
    한글 수식 문자열 → LaTeX 수식 문자열 변환
    """
    tokens = tokenize(expr)
    print(f"[DEBUG] 한글 토큰: {tokens}")
    return render_hangul_to_latex(tokens)


def parse_latex_to_hangul(expr: str) -> str:
    """
    LaTeX 수식 문자열 → 한글 수식 문자열 변환
    """
    tokens = tokenize(expr)
    print(f"[DEBUG] LaTeX 토큰: {tokens}")
    return render_latex_to_hangul(tokens)