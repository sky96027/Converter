# converter/nodes/cases.py

from converter.base import ExprNode
from converter.mapping.map import HANGUL_TO_LATEX_CASES, LATEX_TO_HANGUL_CASES
from converter.nodes.binary_op import BinaryOpNode


class CasesNode(ExprNode):
    """
    케이스 분할 수식 표현 노드 (예: \begin{cases} ... \end{cases})
    """

    def __init__(self, op, *args):
        from converter.parser import build_ast, tokenize  # 순환 import 회피

        self.op = HANGUL_TO_LATEX_CASES.get(op, op)
        self.args = []

        if len(args) == 1 and isinstance(args[0], ExprNode) and hasattr(args[0], "value"):
            raw_content = args[0].value.strip("{} ")
            lines = raw_content.split("#")
            for line in lines:
                if "&&" in line:
                    left_raw, right_raw = line.split("&&", 1)
                    left_ast = build_ast(tokenize(left_raw.strip()), from_lang="HANGUL", to_lang="LATEX")
                    right_ast = build_ast(tokenize(right_raw.strip()), from_lang="HANGUL", to_lang="LATEX")
                    self.args.append(BinaryOpNode("&", left_ast, right_ast))
        else:
            self.args = list(args)

    def to_latex(self) -> str:
        content = r" \\ ".join(arg.to_latex() for arg in self.args)
        return f"\\begin{{cases}} {content} \\end{{cases}}"

    def to_hangul(self) -> str:
        hangul_op = LATEX_TO_HANGUL_CASES.get(self.op, self.op)
        content = " # ".join(arg.to_hangul() for arg in self.args)
        return f"{hangul_op} {content}"

    def __repr__(self):
        return f"CasesNode('{self.op}', {', '.join(repr(a) for a in self.args)})"