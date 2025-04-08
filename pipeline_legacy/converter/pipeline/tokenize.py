# converter/pipeline/tokenize.py
import re

def tokenize_hangul(expr: str) -> list[str]:
    """
    한글 수식 문자열을 공백 단위로 분할하여 토큰 리스트 생성

    예:
        'SIN x' → ['SIN', 'x']
    """
    return expr.strip().split()


def tokenize_latex(expr: str) -> list[str]:
    """
    LaTeX 수식 문자열을 토큰 리스트로 변환

    1. \command       → ex: \frac, \sin, \geq
    2. _{...}, ^{...} → 제어기호 병합 토큰 분리
    3. {...}, [...]   → 괄호 그룹 유지
    4. 단일 연산자    → + - * / = < > 등

    예:
        '\\int_{0}^{1} x dx'
        → ['\\int', '_', '{0}', '^', '{1}', 'x', 'dx']
    """
    tokens = []

    # 정규식 패턴 정의, 수식 추가 시 유지 보수가 우려되지만 비용 대비 최선인듯 함
    pattern = r'(\\[a-zA-Z]+|[_^]{1}\{[^}]*\}|\{[^}]*\}|\[[^\]]*\]|[=+\-*/^_<>]|[a-zA-Z0-9]+)'

    for match in re.finditer(pattern, expr):
        token = match.group()

        # '_{...}' → ['_', '{...}']
        if token.startswith('_') and token[1] == '{':
            tokens.extend(['_', token[1:]])

        # '^{...}' → ['^', '{...}']
        elif token.startswith('^') and token[1] == '{':
            tokens.extend(['^', token[1:]])

        else:
            tokens.append(token)

    return tokens


def tokenize(expr: str) -> list[str]:
    """
    Wrapper: 입력이 LaTeX인지 한글인지 판단해서 자동 분기
    """
    expr = expr.strip()
    if expr.startswith("\\") or "{" in expr or "}" in expr:
        return tokenize_latex(expr)
    else:
        return tokenize_hangul(expr)