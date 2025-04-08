# converter/mapping/precedence.py

"""
이 모듈은 LaTeX <-> 한글 수식 변환에서 사용되는 연산자 우선순위를 정의합니다.

- HANGUL 수식 → LATEX 변환 시: OP_PRECEDENCE_HANGUL 사용
- LATEX 수식 → HANGUL 변환 시: OP_PRECEDENCE_LATEX 사용

우선순위는 수식 내 연산자 간 결합 구조를 판단하여 AST 트리를 구성하는 데 사용됩니다.
값이 작을수록 우선순위가 낮으며, 트리 상위 노드로 먼저 분기됩니다.

예시:
- x + y * z → ×가 +보다 우선순위 높음 → y * z 먼저 결합

단항 연산자 및 함수 (`log`, `sqrt`, `lim` 등)도 내부 구조가 존재하므로 포함됩니다.
"""

OP_PRECEDENCE_HANGUL = {
    "=": 0,
    "+": 1,
    "-": 1,
    "ge": 1,
    "le": 1,
    "ne": 1,
    "times": 2,
    "div": 2,
    "over": 3,
    "^": 4,

    "log": 5,
    "sqrt": 5,
    "lim": 5,
    "int": 5,

    "sum": 6,
    "prod": 6,
    "cup": 6,
    "smallinter": 6,
    "cases": 6,

    "rarrow": 7,
    "mapsto": 7,

    "prime": 8,
    "doubleprime": 8,
}

OP_PRECEDENCE_LATEX = {
    "=": 0,
    "+": 1,
    "-": 1,
    r"\ge": 1,
    r"\le": 1,
    r"\ne": 1,
    r"\times": 2,
    r"\div": 2,
    r"\frac": 3,
    "^": 4,

    r"\log": 5,
    r"\sqrt": 5,
    r"\lim": 5,
    r"\int": 5,

    r"\sum": 6,
    r"\prod": 6,
    r"\cup": 6,
    r"\cap": 6,
    r"\begin{cases}": 6,

    r"\to": 7,
    r"\mapsto": 7,

    "'": 8,
    "''": 8,
}