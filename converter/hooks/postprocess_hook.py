# converter/hooks/postprocess_hooks.py

import re
from converter.nodes.binary_op import BinaryOpNode
from converter.nodes.derivative import DerivativeNode
from converter.nodes.literal import LiteralNode
from converter.base import ExprNode

def handle_postfix_derivatives(ast: ExprNode) -> ExprNode:
    """
    AST 내 후위 연산자(미분 및 중괄호 등)를 재정렬하거나 치환하는 후처리 훅

    - prime f → f PRIME (DerivativeNode 위치 재조정)
    - prime prime f → f DOUBLEPRIME
    """
    def recurse(node: ExprNode) -> ExprNode:
        if isinstance(node, DerivativeNode) and len(node.args) == 1:
            target = node.args[0]
            if isinstance(target, DerivativeNode):
                return DerivativeNode("''", target.args[0])
            elif isinstance(target, LiteralNode):
                return DerivativeNode(node.op, target)

        if hasattr(node, 'args'):
            node.args = [recurse(child) for child in node.args]
        elif hasattr(node, 'base') and hasattr(node, 'sub'):
            node.base = recurse(node.base)
            node.sub = recurse(node.sub)
        elif hasattr(node, 'children'):
            node.children = [recurse(child) for child in node.children]

        return node
    return recurse(ast)

def handle_cases_structure(ast: ExprNode) -> ExprNode:
    """
    \begin{cases} 내부 표현을 정리하여 CASES 구조에 맞게 변환
    - 내부 줄 구분자: # (ex. a & b # c & d)
    - 이를 children 리스트로 변환해 재구조화할 수 있음
    """
    def recurse(node: ExprNode) -> ExprNode:
        if hasattr(node, 'args'):
            node.args = [recurse(child) for child in node.args]
        elif hasattr(node, 'children'):
            node.children = [recurse(child) for child in node.children]

        if node.__class__.__name__ == 'CasesNode' and len(node.args) == 1:
            only_arg = node.args[0]
            if isinstance(only_arg, LiteralNode):
                rows = only_arg.value.split('#')
                node.children = [LiteralNode(row.strip()) for row in rows]
                node.args = []
        return node
    return recurse(ast)

def handle_matrix_structure(ast: ExprNode) -> ExprNode:
    """
    \begin{matrix} 형태의 행렬 수식을 파싱하여
    행(row)과 열(column)을 명확히 분리된 children 구조로 재구성
    """
    def recurse(node: ExprNode) -> ExprNode:
        if hasattr(node, 'args'):
            node.args = [recurse(child) for child in node.args]
        elif hasattr(node, 'children'):
            node.children = [recurse(child) for child in node.children]

        if node.__class__.__name__ == 'MatrixNode' and len(node.args) == 1:
            only_arg = node.args[0]
            if isinstance(only_arg, LiteralNode):
                rows = only_arg.value.split('#')
                matrix = []
                for row in rows:
                    cols = [LiteralNode(col.strip()) for col in row.split('&')]
                    matrix.append(cols)
                node.children = matrix
                node.args = []
        return node
    return recurse(ast)

def handle_nested_mix(ast: ExprNode) -> ExprNode:
    """
    복합 중첩 수식 구조 정제 (예: 적분 안에 분수/로그 등)
    - 불필요한 LiteralNode 중첩 제거
    - 연산자 우선 순서나 깊이 조정 (단순화)
    """
    def unwrap_literal(node: ExprNode) -> ExprNode:
        if isinstance(node, LiteralNode):
            val = node.value.strip()
            if val.startswith('{') and val.endswith('}'):
                return LiteralNode(val[1:-1])
        return node

    def recurse(node: ExprNode) -> ExprNode:
        if hasattr(node, 'args'):
            node.args = [unwrap_literal(recurse(child)) for child in node.args]
        elif hasattr(node, 'children'):
            node.children = [unwrap_literal(recurse(child)) for child in node.children]
        return node
    return recurse(ast)

def handle_vector_classification(ast: ExprNode) -> ExprNode:
    """
    \vec / \hat 처리 후 벡터 / 단위벡터를 정확히 구분
    - \vec → VEC
    - \hat → UNIT
    """
    def recurse(node: ExprNode) -> ExprNode:
        if node.__class__.__name__ == 'VectorNode':
            if node.op == r'\vec':
                node.kind = 'vec'
            elif node.op == r'\hat':
                node.kind = 'unit'
        if hasattr(node, 'args'):
            node.args = [recurse(child) for child in node.args]
        elif hasattr(node, 'children'):
            node.children = [recurse(child) for child in node.children]
        return node
    return recurse(ast)

def merge_negative_numbers(tokens: list[str]) -> list[str]:
    merged = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '-' and i + 1 < len(tokens):
            next_tok = tokens[i + 1]
            # 다음 토큰이 숫자이거나 변수명 (예: x, 3, 2.5 등)
            if re.fullmatch(r'\d+(\.\d+)?|[a-zA-Z]', next_tok):
                merged.append('-' + next_tok)
                i += 2
                continue
        merged.append(tokens[i])
        i += 1
    return merged

def apply_postprocess_hooks(ast: ExprNode) -> ExprNode:
    """
    후처리 훅 전체를 AST에 순차 적용하는 통합 진입점 함수
    """
    hooks = [
        handle_postfix_derivatives,
        handle_cases_structure,
        handle_matrix_structure,
        handle_nested_mix,
        handle_vector_classification,
    ]
    for hook in hooks:
        ast = hook(ast)
    return ast

