# converter/pipeline/render.py

from converter.pipeline.hangul_lookup import get_latex_token_from_hangul
from converter.pipeline.latex_lookup import get_hangul_token_from_latex


def strip_braces(token: str) -> str:
    """중괄호나 대괄호로 감싸진 토큰에서 내용만 추출"""
    if token.startswith('{') and token.endswith('}'):
        return token[1:-1]
    if token.startswith('[') and token.endswith(']'):
        return token[1:-1]
    return token


def render_latex_to_hangul(tokens: list[str]) -> str:
    """
    LaTeX 토큰 리스트를 한글 수식 문자열로 렌더링

    - 한글 수식은 띄어쓰기 기반 구문 형식을 따르므로,
      각 변환된 토큰을 공백(" ")으로 연결하여 문자열을 구성한다.
    - 예: ['1', '+', '2'] → ['1', 'PLUS', '2'] → '1 PLUS 2'

    반환값: 한글 수식 문자열 (str)
    """
    converted = [get_hangul_token_from_latex(token) for token in tokens]
    return " ".join(converted)


def render_hangul_to_latex(tokens: list[str]) -> str:
    """
    한글 토큰 리스트를 LaTeX 수식 문자열로 렌더링

    - LaTeX 수식은 함수(예: \frac, \sin 등)와 인자({3}, {x}) 사이에
      공백이 없어야 하므로, 각 토큰의 종류에 따라 공백 삽입 여부를 조건부로 제어한다.
    - 함수형 표현(\sin, \cos, \tan, \log 등)의 경우 다음 토큰이 일반 리터럴이면
      반드시 중괄호({})로 감싸서 출력한다.

    예:
        ['FRAC', '{3}', '{4}']     → '\\frac{3}{4}'
        ['SIN', 'x']               → '\\sin{x}'
        ['PLUS', '2']              → '+ 2'

    반환값: LaTeX 수식 문자열 (str)
    """
    converted = [get_latex_token_from_hangul(token) for token in tokens]
    output = ""
    for i, token in enumerate(converted):
        if i == 0:
            output += token
            continue

        prev_token = converted[i - 1]

        # 함수 뒤 인자: 중괄호로 감싸기
        if prev_token in {"\\sin", "\\cos", "\\tan", "\\log"} and not token.startswith(("{", "[")):
            output += "{" + token + "}"

        # 함수나 연산자 뒤 중괄호/대괄호 → 공백 없이 붙임
        elif prev_token.startswith("\\") and token.startswith(("{", "[")):
            output += token

        # 단독 중괄호/대괄호도 공백 없이 붙임
        elif token.startswith(("{", "[")):
            output += token

        # 일반 경우 → 공백 삽입
        else:
            output += " " + token

    return output