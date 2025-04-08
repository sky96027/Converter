# converter/parser.py

"""
이 모듈은 Hangul <-> LaTeX 수식 변환을 위한 파서를 구현합니다.

모듈 개발 시 최우선 기준 :
- 수식 변환시 수식의 '의미' 보존에 중점
- 변환 시 정보 소실을 방지하여야 함
- ex ) x^{n+1} -> x^n+1 -> x^{n}+1 중괄호 고려를 하지 않으면 2회전 이상 변환 시 되면 기존 수식이 가지던 의미를 파괴하게 됨


핵심 기능:
- 입력된 수식 문자열을 토큰 단위로 분리 (`tokenize`)
- 토큰 리스트를 기반으로 AST(Abstract Syntax Tree) 구성 (`build_ast`)
- 자동 괄호(left/right), RootNode(sqrt of 구조) 등 특수한 구문 처리 포함
- 매핑 테이블 및 노드 클래스 기반으로 다양한 수식 구조 생성
- 후처리 훅(`apply_postprocess_hooks`)을 통해 AST 정제 처리

사용 예시:
- `parse_hangul("sqrt{3}of{5}")` → LaTeX AST 반환
- `parse_latex("\\sqrt[3]{5}")` → 한글 AST 반환

의존 모듈:
- converter.nodes.* (각종 수식 노드)
- converter.mapping.map (언어 간 매핑 정보)
- converter.hooks.postprocess_hook (후처리 훅)

주의 사항:
- sqrt of 구조는 파서 내부에서 직접 분기 처리
- 자동 괄호는 left/right 접두어를 기반으로 BracketNode 생성
"""

import logging
from converter.base import ExprNode
from converter.nodes.literal import LiteralNode
from converter.utils.string_util import to_pascal_case
from converter.hooks.postprocess_hook import apply_postprocess_hooks, merge_negative_numbers

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s parser] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 모든 노드 클래스 import (리플렉션 동작 보장)
from converter.nodes.root import RootNode
from converter.nodes.log import LogNode
from converter.nodes.function import FunctionNode
from converter.nodes.fraction import FractionNode
from converter.nodes.integral import IntegralNode
from converter.nodes.bigop import BigOpNode
from converter.nodes.matrix import MatrixNode
from converter.nodes.limit import LimitNode
from converter.nodes.cases import CasesNode
from converter.nodes.arrow import ArrowNode
from converter.nodes.vector import VectorNode
from converter.nodes.derivative import DerivativeNode
from converter.nodes.bracket import BracketNode
from converter.nodes.binary_op import BinaryOpNode
from converter.nodes.power import PowerNode

# 매핑 import
from converter.mapping.map import *
from converter.mapping.precedence import OP_PRECEDENCE_HANGUL, OP_PRECEDENCE_LATEX


def tokenize(expr: str) -> list[str]:
    def collect_brace_block(expr: str, start_index: int) -> tuple[str, int]:
        i = start_index
        brace_depth = 1
        block = '{'
        while i < len(expr) and brace_depth > 0:
            if expr[i] == '{':
                brace_depth += 1
            elif expr[i] == '}':
                brace_depth -= 1
            block += expr[i]
            i += 1
        return block, i

    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        # Hangul 자동 괄호: LEFT ( → left(
        if expr[i:i + 4].upper() == "LEFT" and i + 4 < len(expr) and expr[i + 4] in '(){}[]':
            tokens.append("left")
            tokens.append(expr[i + 4])
            i += 5
            continue
        if expr[i:i + 5].upper() == "RIGHT" and i + 5 < len(expr) and expr[i + 5] in '(){}[]':
            tokens.append("right")
            tokens.append(expr[i + 5])
            i += 6
            continue

        # LaTeX 자동 괄호: \left( → \left(
        if expr.startswith(r'\left', i) and i + 6 <= len(expr) and expr[i + 5] in '(){}[]':
            tokens.append(r'\left')
            tokens.append(expr[i + 5])
            i += 6
            continue
        if expr.startswith(r'\right', i) and i + 7 <= len(expr) and expr[i + 6] in '(){}[]':
            tokens.append(r'\right')
            tokens.append(expr[i + 6])
            i += 7
            continue

        # 중괄호 블록
        if ch == '{':
            block, i = collect_brace_block(expr, i + 1)
            tokens.append(block)
            continue

        if ch == ' ':
            i += 1
            continue

        # 알파벳 연속 토큰
        if ch.isalpha():
            ident = ''
            while i < len(expr) and expr[i].isalpha():
                ident += expr[i]
                i += 1
            tokens.append(ident)
            continue

        # LaTeX 명령어
        if ch == '\\':
            command = ch
            i += 1
            #while i < len(expr) and (expr[i].isalpha() or expr[i] == '_'):
            while i < len(expr) and expr[i].isalpha():
                command += expr[i]
                i += 1
            tokens.append(command)
            continue

        # 단일 문자 토큰 (괄호 등)
        tokens.append(ch)
        i += 1

    tokens = merge_negative_numbers(tokens)

    print(f"[DEBUG tokenize] 입력: {expr}")
    print(f"[DEBUG tokenize] 결과 토큰: {tokens}")

    return tokens

def merge_brackets(tokens: list[str]) -> list[str]:
    """
    LaTeX에서 [3]을 [ '3' ]로 나누는 현상 방지용
    [ → '[3]' 으로 병합
    토큰 전처리이기 때문에 parser 내부에 위치시킴
    """
    merged = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "[" and i + 2 < len(tokens) and tokens[i + 2] == "]":
            merged.append(f"[{tokens[i + 1]}]")
            i += 3
        else:
            merged.append(tokens[i])
            i += 1
    return merged

def find_lowest_precedence_op(tokens: list[str], from_lang: str, to_lang: str) -> tuple[int, str]:
    """
    핵심 분기 로직
    수식 토큰에서 가장 낮은 우선순위 연산자의 인덱스와 해당 맵 이름을 반환
    - BinaryOpNode, FractionNode, PowerNode 등 모든 이항 연산 처리에 사용됨
    - 우선순위는 OP_PRECEDENCE_*** 에 정의된 값을 기준으로 비교
    """
    from converter.mapping.precedence import OP_PRECEDENCE_HANGUL, OP_PRECEDENCE_LATEX

    precedence_map = (
        OP_PRECEDENCE_HANGUL if from_lang.upper() == "HANGUL"
        else OP_PRECEDENCE_LATEX
    )

    prefix = f"{from_lang.upper()}_TO_{to_lang.upper()}_"
    map_candidates = [name for name in globals() if name.startswith(prefix)]

    min_prec = float("inf")
    min_index = -1
    min_map_name = ""

    for i, tok in enumerate(tokens):
        for map_name in map_candidates:
            map_dict = globals()[map_name]
            if tok in map_dict:
                prec = precedence_map.get(tok, float("inf"))
                if prec <= min_prec:
                    min_prec = prec
                    min_index = i
                    min_map_name = map_name

    return min_index, min_map_name

def should_skip_reflection(tokens: list[str]) -> bool:
    """
    다음과 같은 경우 우선순위 기반 분기를 건너뛰어야 함:
    1. 자동 괄호 구조 포함 (BracketNode)
    2. RootNode 특수 분기 - 인자가 두 개인 경우만 (e.g., \sqrt[3]{x}, sqrt {3} of {x})
    """
    # 1. BracketNode 관련 토큰이 포함되어 있는 경우
    if any(tok in HANGUL_TO_LATEX_BRACKET for tok in tokens) or any(tok in LATEX_TO_HANGUL_BRACKET for tok in tokens):
        return True

    # 2. RootNode LaTeX (\sqrt[3]{x})
    if tokens[0] == r"\sqrt" and len(tokens) == 3 and tokens[1].startswith("[") and tokens[2].startswith("{"):
        return True

    # 3. RootNode Hangul (sqrt {3} of {x})
    if tokens[0] == "sqrt" and "of" in tokens and len(tokens) > 2:
        return True

    # === IntegralNode 구조  ===
    if tokens[0] in ["int", "\\int"] and "_" in tokens and "^" in tokens and any(
            t.endswith("dx") or t == "dx" for t in tokens):
        return True

    return False


def extract_bracket_node_once(tokens: list[str], from_lang: str, to_lang: str):
    """
    수식 내 하나의 괄호 쌍만 찾아서 BracketNode로 감싸고, 감싼 토큰 리스트를 반환
    - BracketNode 감싼 부분을 치환한 새 토큰 리스트 반환
    - 감싸지 못하면 None 반환
    """
    for i in range(len(tokens)):
        if isinstance(tokens[i], str) and (
                tokens[i].lower().startswith("left") or tokens[i].lower().startswith(r"\left")):
            for j in range(i + 2, len(tokens)):
                if isinstance(tokens[j], str) and (
                        tokens[j].lower().startswith("right") or tokens[j].lower().startswith(r"\right")):
                    lparen = tokens[i][4:] if tokens[i].lower().startswith("left") else tokens[i][5:]
                    rparen = tokens[j][5:] if tokens[j].lower().startswith("right") else tokens[j][6:]

                    left_tag = r"\left" if tokens[i].lower().startswith("left") else tokens[i]
                    right_tag = r"\right" if tokens[j].lower().startswith("right") else tokens[j]

                    # 내부 노드 처리 개선
                    inner_tokens = tokens[i + 1:j]
                    if len(inner_tokens) == 1 and isinstance(inner_tokens[0], str):
                        # 단일 LiteralNode인 경우 괄호를 제외한 내용만 추출
                        inner_value = inner_tokens[0].strip()
                        if inner_value.startswith(lparen) and inner_value.endswith(rparen):
                            inner_value = inner_value[1:-1].strip()
                        inner_ast = LiteralNode(inner_value)
                    else:
                        inner_ast = build_ast(inner_tokens, from_lang, to_lang)

                    bracket_ast = BracketNode(left_tag, lparen, inner_ast, rparen, right_tag)

                    # 치환된 새 토큰 리스트 반환
                    return tokens[:i] + [bracket_ast] + tokens[j + 1:]
    return None


def build_ast(tokens: list[str], from_lang: str, to_lang: str) -> ExprNode:
    print(f"[DEBUG build_ast] 받은 토큰: {tokens}")
    if not tokens:
        return LiteralNode("")

    # === 재귀적으로 BracketNode 처리 ===
    while True:
        new_tokens = extract_bracket_node_once(tokens, from_lang, to_lang)
        if new_tokens is None:
            break
        tokens = new_tokens

    # === 특수 구조 우선 분기 ===
    if tokens[0] == r"\sqrt" and len(tokens) == 3 and tokens[1].startswith("[") and tokens[2].startswith("{"):
        index_ast = build_ast(tokenize(tokens[1][1:-1]), from_lang, to_lang)
        value_ast = build_ast(tokenize(tokens[2][1:-1]), from_lang, to_lang)
        return RootNode(r"\sqrt", index_ast, value_ast)

    if tokens[0] == "sqrt" and "of" in tokens:
        idx = tokens.index("of")
        left_ast = build_ast(tokens[1:idx], from_lang, to_lang)
        right_ast = build_ast(tokens[idx+1:], from_lang, to_lang)
        return RootNode(r"\sqrt", left_ast, right_ast)

    if (tokens[0].startswith("int") or tokens[0].startswith("\\int")) \
            and any("_" in t for t in tokens) and any("^" in t for t in tokens) and any("dx" in t for t in tokens):
        try:
            underscore_index = next(i for i, t in enumerate(tokens) if "_" in t)
            caret_index = next(i for i, t in enumerate(tokens) if "^" in t)
            lower = tokens[underscore_index + 1].strip("{} ")
            upper = tokens[caret_index + 1].strip("{} ")
            body_tokens = tokens[caret_index + 2:-1]
            dx_token = tokens[-1].replace("`", "").replace("\\,", "").strip()
            body_tokens = [t for t in body_tokens if t not in [r"\,", r"\;", r"\!", r"\\,", "\\", ","]]

            return IntegralNode(
                tokens[0],
                build_ast(tokenize(lower), from_lang, to_lang),
                build_ast(tokenize(upper), from_lang, to_lang),
                build_ast(body_tokens, from_lang, to_lang),
                build_ast([dx_token], from_lang, to_lang)
            )
        except Exception as e:
            logger.warning(f"[IntegralNode Parsing] Failed: {tokens} - {e}")

    if len(tokens) == 1:
        return LiteralNode(tokens[0])

    if not should_skip_reflection(tokens):
        op_index, map_name = find_lowest_precedence_op(tokens, from_lang, to_lang)

        if op_index != -1 and map_name:
            op = tokens[op_index]
            map_type = map_name.replace(f"{from_lang.upper()}_TO_{to_lang.upper()}_", "")
            class_name = to_pascal_case(map_type) + "Node"
            cls = globals().get(class_name)

            if cls:
                # 함수형 연산자
                if op_index == 0:
                    args = [build_ast(tokenize(t[1:-1]) if t.startswith("{") else [t], from_lang, to_lang)
                            for t in tokens[1:]]
                    return cls(op, *args)
                # 이항 연산자
                left = build_ast(tokens[:op_index], from_lang, to_lang)
                right = build_ast(tokens[op_index + 1:], from_lang, to_lang)
                return cls(op, left, right)

    # fallback: 첫 토큰 기준 리플렉션
    first = tokens[0]
    prefix = f"{from_lang.upper()}_TO_{to_lang.upper()}_"
    for map_name in [name for name in globals() if name.startswith(prefix)]:
        map_dict = globals()[map_name]
        if first in map_dict:
            class_name = to_pascal_case(map_name.replace(prefix, "")) + "Node"
            cls = globals().get(class_name)
            if cls and class_name != "BracketNode":
                args = [build_ast(tokenize(t[1:-1]) if t.startswith("{") else [t], from_lang, to_lang)
                        for t in tokens[1:]]
                return cls(first, *args)

    # 마지막 fallback
    return LiteralNode(" ".join(str(t) if isinstance(t, str) else repr(t) for t in tokens))


# def build_ast(tokens: list[str], from_lang: str, to_lang: str) -> ExprNode:
#     print(f"[DEBUG build_ast] 받은 토큰: {tokens}")
#     if not tokens:
#         return LiteralNode("")
#
#     # 특수 문법 분기
#     # === 재귀적으로 BracketNode 처리 ===
#     while True:
#         new_tokens = extract_bracket_node_once(tokens, from_lang, to_lang)
#         if new_tokens is None:
#             break
#         tokens = new_tokens
#
#     # root
#     if tokens[0] == r"\sqrt" and len(tokens) == 3 and tokens[1].startswith("[") and tokens[2].startswith("{"):
#         index_token = tokens[1][1:-1]
#         value_token = tokens[2][1:-1]
#         index_ast = build_ast(tokenize(index_token), from_lang, to_lang)
#         value_ast = build_ast(tokenize(value_token), from_lang, to_lang)
#         return RootNode(r"\sqrt", index_ast, value_ast)
#
#     if tokens[0] == "sqrt" and "of" in tokens:
#         idx = tokens.index("of")
#         left_tokens = tokens[1:idx]
#         right_tokens = tokens[idx + 1:]
#         left_ast = build_ast(left_tokens, from_lang, to_lang)
#         right_ast = build_ast(right_tokens, from_lang, to_lang)
#         return RootNode(r"\sqrt", left_ast, right_ast)
#
#     # IntegralNode 처리
#     if (tokens[0].startswith("int") or tokens[0].startswith("\\int")) \
#             and any("_" in t for t in tokens if isinstance(t, str)) \
#             and any("^" in t for t in tokens if isinstance(t, str)) \
#             and any("dx" in t.replace(" ", "") for t in tokens if isinstance(t, str)):
#
#         try:
#             # '_'와 '^'가 포함된 토큰의 실제 위치를 찾아냄
#             underscore_index = next(i for i, t in enumerate(tokens) if isinstance(t, str) and "_" in t)
#             caret_index = next(i for i, t in enumerate(tokens) if isinstance(t, str) and "^" in t)
#
#             # 하한/상한 토큰 파싱
#             lower_token = tokens[underscore_index + 1].strip("{} ").replace(" ", "")
#             upper_token = tokens[caret_index + 1].strip("{} ").replace(" ", "")
#
#             # 본문 및 dx 파트 분리
#             body_tokens = tokens[caret_index + 2:-1]
#             dx_token = tokens[-1]
#
#             # AST 재귀 파싱
#             lower_ast = build_ast(tokenize(lower_token), from_lang, to_lang)
#             upper_ast = build_ast(tokenize(upper_token), from_lang, to_lang)
#             body_ast = build_ast(body_tokens, from_lang, to_lang)
#             dx_ast = build_ast([dx_token.replace("`", "").replace("\\,", "").strip()], from_lang, to_lang)
#
#             return IntegralNode(tokens[0], lower_ast, upper_ast, body_ast, dx_ast)
#
#         except Exception as e:
#             logger.warning(f"[IntegralNode Parsing] Failed to parse integral structure: {tokens} - {e}")
#             pass
#
#     # bracket ( 최후 조건 )
#     if len(tokens) >= 3:
#         print(f"[DEBUG Bracket 분기 진입 후보] {tokens}")
#         first, *middle, last = tokens
#         if (first.lower().startswith("left") or first.lower().startswith(r"\left")) and \
#                 (last.lower().startswith("right") or last.lower().startswith(r"\right")) and \
#                 len(first) > 4 and len(last) > 5:
#             lparen = first[4:] if first.lower().startswith("left") else first[5:]
#             rparen = last[5:] if last.lower().startswith("right") else last[6:]
#
#             left_tag = r"\left" if first.lower().startswith("left") else first
#             right_tag = r"\right" if last.lower().startswith("right") else last
#
#             inner_ast = build_ast(middle, from_lang, to_lang)
#             return BracketNode(left_tag, lparen, inner_ast, rparen, right_tag)
#
#
#
#     if len(tokens) == 1:
#         return LiteralNode(tokens[0])
#
#     if not should_skip_reflection(tokens):
#         # 우선순위 기반 리플렉션 분기
#         op_index, map_name = find_lowest_precedence_op(tokens, from_lang, to_lang)
#
#         if op_index != -1 and map_name:
#             op = tokens[op_index]
#             map_type = map_name.replace(f"{from_lang.upper()}_TO_{to_lang.upper()}_", "")
#             class_name = to_pascal_case(map_type) + "Node"
#             cls = globals().get(class_name)
#
#             # 1. 함수형 연산자 (prefix)
#             if op_index == 0 and cls is not None:
#                 args = []
#                 for t in tokens[1:]:
#                     if t.startswith("{") and t.endswith("}"):
#                         inner = t[1:-1]
#                         inner_tokens = tokenize(inner)
#                         args.append(build_ast(inner_tokens, from_lang, to_lang))
#                     else:
#                         args.append(build_ast([t], from_lang, to_lang))
#                 return cls(op, *args)
#
#             # 2. 이항 연산자 (infix)
#             if cls is not None:
#                 left_tokens = tokens[:op_index]
#                 right_tokens = tokens[op_index + 1:]
#                 left_ast = build_ast(left_tokens, from_lang, to_lang)
#                 right_ast = build_ast(right_tokens, from_lang, to_lang)
#                 return cls(op, left_ast, right_ast)
#
#     # fallback: 기본 리플렉션 분기 (단항 연산자 또는 리터럴 묶음)
#     first_raw = tokens[0]
#     first = first_raw.lower()
#     prefix = f"{from_lang.upper()}_TO_{to_lang.upper()}_"
#     map_candidates = [name for name in globals() if name.startswith(prefix)]
#
#     for map_name in map_candidates:
#         map_dict = globals()[map_name]
#         if first in map_dict:
#             token_type = map_name.replace(prefix, "")
#             class_name = to_pascal_case(token_type) + "Node"
#
#             if class_name == "BracketNode":
#                 continue
#
#             cls = globals().get(class_name)
#             if cls is not None:
#                 args = []
#                 for t in tokens[1:]:
#                     if t.startswith("{") and t.endswith("}"):
#                         inner = t[1:-1]
#                         inner_tokens = tokenize(inner)
#                         args.append(build_ast(inner_tokens, from_lang, to_lang))
#                     else:
#                         args.append(build_ast([t], from_lang, to_lang))
#                 return cls(first, *args)
#
#     if all(isinstance(tok, str) for tok in tokens):
#         return LiteralNode(" ".join(tokens))
#     else:
#         # BracketNode 등 객체가 섞여 있는 경우 repr로 안전하게 처리
#         safe_tokens = [tok if isinstance(tok, str) else repr(tok) for tok in tokens]
#         return LiteralNode(" ".join(safe_tokens))


def parse_hangul(text: str) -> ExprNode:
    tokens = tokenize(text)
    ast = build_ast(tokens, from_lang="HANGUL", to_lang="LATEX")
    return apply_postprocess_hooks(ast)


def parse_latex(expr: str) -> ExprNode:
    tokens = tokenize(expr)
    tokens = merge_brackets(tokens)  # 전처리
    ast = build_ast(tokens, from_lang="LATEX", to_lang="HANGUL")
    return apply_postprocess_hooks(ast)