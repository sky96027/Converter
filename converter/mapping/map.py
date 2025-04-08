# converter/mapping/map.py

# =========================
# 루트 연산자 (Root)
# =========================
HANGUL_TO_LATEX_ROOT = {
    'sqrt': r'\sqrt',
}
LATEX_TO_HANGUL_ROOT = {
    r'\sqrt': 'sqrt',
}

# =========================
# 로그 (Log)
# =========================
HANGUL_TO_LATEX_LOG = {
    'log': r'\log',
}
LATEX_TO_HANGUL_LOG = {
    r'\log': 'log',
}

# =========================
# 함수(Function) — sin, cos, tan 등
# =========================
HANGUL_TO_LATEX_FUNCTION = {
    'sin': r'\sin',
    'cos': r'\cos',
    'tan': r'\tan',
}
LATEX_TO_HANGUL_FUNCTION = {
    r'\sin': 'sin',
    r'\cos': 'cos',
    r'\tan': 'tan',
}

# =========================
# 분수(Fraction)
# =========================
HANGUL_TO_LATEX_FRACTION = {
    'over': r'\frac',
}
LATEX_TO_HANGUL_FRACTION = {
    r'\frac': 'over',
}

# =========================
# 지수 표현 (Power) -> 양 쪽 다 ^기 때문에 불필요할 수 있음 하지만 일관성 유지 선택
# 일관성 선택 이유 : 확장성 - 다른 기호 추가시, 구조 유지 - reflection
# =========================
HANGUL_TO_LATEX_POWER = {
    '^': '^',
}
LATEX_TO_HANGUL_POWER = {
    '^': '^',
}

# =========================
# 적분 연산자 (Integral Variants)
# =========================
HANGUL_TO_LATEX_INTEGRAL = {
    'int': r'\int',
}

LATEX_TO_HANGUL_INTEGRAL = {
    r'\int': 'int',
}

# =========================
# 분할 수식 (Cases)
# =========================
HANGUL_TO_LATEX_CASES = {
    'cases': r'\begin{cases}',
}
LATEX_TO_HANGUL_CASES = {
    r'\begin{cases}': 'cases',
}

# 화살표 매핑 (arrow)
HANGUL_TO_LATEX_ARROW = {
    'rarrow': r'\to',         # XML에선 rarrow로 들어옴
    'mapsto': r'\mapsto',
}
LATEX_TO_HANGUL_ARROW = {
    r'\to': 'rarrow',
    r'\mapsto': 'mapsto',
}

# =========================
# 벡터/단위벡터 기호
# =========================
HANGUL_TO_LATEX_VECTOR = {
    'vec': r'\vec',       # 벡터
    'unit': r'\hat',      # 단위벡터
}
LATEX_TO_HANGUL_VECTOR = {
    r'\vec': 'vec',
    r'\hat': 'unit',
}

# =========================
# 미분 (Derivatives)
# =========================
HANGUL_TO_LATEX_DERIV = {
    'prime': "'",
    'doubleprime': "''",
}
LATEX_TO_HANGUL_DERIV = {
    "'": 'prime',
    "''": 'doubleprime',
}

# =========================
# 집합 중괄호 표현 (Set Brackets) – 후처리 hook 고려
# =========================
HANGUL_TO_LATEX_SET = {
    '{': '{',
    '}': '}',
}
LATEX_TO_HANGUL_SET = {
    '{': '{',
    '}': '}',
}

# =========================
# 누산/집합 기호 (Big Operators)
# =========================
HANGUL_TO_LATEX_BIGOP = {
    'sum': r'\sum',      # 총합
    'prod': r'\prod',    # 파이
    'cup': r'\cup',    # 합집합
    'smallinter': r'\cap',    # 교집합
}

LATEX_TO_HANGUL_BIGOP = {
    r'\sum': 'sum',
    r'\prod': 'prod',
    r'\cup': 'union',
    r'\cap': 'inter',
}

# =========================
# 행렬(Matrix) 표현
# =========================

# 한글 → LaTeX
HANGUL_TO_LATEX_MATRIX = {
    'matrix': r'\begin{matrix}',
    'pmatrix': r'\begin{pmatrix}',
    'bmatrix': r'\begin{bmatrix}',
    'dmatrix': r'\begin{vmatrix}',
}

# # LaTeX → 한글
LATEX_TO_HANGUL_MATRIX = {
    r'\begin{matrix}': 'matrix',
    r'\begin{pmatrix}': 'pmatrix',
    r'\begin{bmatrix}': 'bmatrix',
    r'\begin{vmatrix}': 'dmatrix',
}

# =========================
# 극한(Limit)
# =========================
HANGUL_TO_LATEX_LIMIT = {
    'lim': r'\lim',
}
LATEX_TO_HANGUL_LIMIT = {
    r'\lim': 'lim',
}

# =========================
# 이항 연산자(BinaryOp)
# =========================
HANGUL_TO_LATEX_BINARY_OP = {
    'times': r'\times',
    'div': r'\div',
    'ge': r'\ge',
    'le': r'\le',
    'ne': r'\ne',
}
LATEX_TO_HANGUL_BINARY_OP = {
    r'\times': 'times',
    r'\div': 'div',
    r'\ge': 'ge',
    r'\le': 'le',
    r'\ne': 'ne',
}

# =========================
# 괄호 표현 (BracketNode)
# =========================
LATEX_TO_HANGUL_BRACKET = {
    r'\left': 'left',
    r'\right': 'right',
    r'\left(': 'left(',
    r'\right)': 'right)',
    r'\left[': 'left[',
    r'\right]': 'right]',
    r'\left{': 'left{',
    r'\right}': 'right}',
    '(': '(',
    ')': ')',
}
HANGUL_TO_LATEX_BRACKET = {
    'left': r'\left',
    'right': r'\right',
    'left(': r'\left(',
    'right)': r'\right)',
    'left[': r'\left[',
    'right]': r'\right]',
    'left{': r'\left{',
    'right}': r'\right}',
    '(': '(',
    ')': ')',
}

# =========================
# 막대 표시 (Bar) – 구조성 있음 → BarNode
# =========================
HANGUL_TO_LATEX_BAR = {
    'bar': r'\bar',
}
LATEX_TO_HANGUL_BAR = {
    r'\bar': 'bar',
}

# =========================
# 각도 기호 (Angle) – 구조성 있음 → Angle
# =========================
HANGUL_TO_LATEX_ANGLE = {
    'angle': r'\angle',
}
LATEX_TO_HANGUL_ANGLE = {
    r'\angle': 'angle',
}

# =========================
# 기호(Symbol)표현 ( 구조성이 없는 )
# =========================
HANGUL_TO_LATEX_SYMBOL = {
    'alpha': r'\alpha',
    'beta': r'\beta',
    'gamma': r'\gamma',
    'delta': r'\delta',
    'epsilon': r'\epsilon',
    'zeta': r'\zeta',
    'eta': r'\eta',
    'theta': r'\theta',
    'iota': r'\iota',
    'kappa': r'\kappa',
    'lambda': r'\lambda',
    'mu': r'\mu',
    'nu': r'\nu',
    'xi': r'\xi',
    'omicron': r'o',         # LaTeX에서는 별도 기호 없이 문자 'o' 사용
    'pi': r'\pi',
    'rho': r'\rho',
    'sigma': r'\sigma',
    'tau': r'\tau',
    'upsilon': r'\upsilon',
    'phi': r'\phi',
    'chi': r'\chi',
    'psi': r'\psi',
    'omega': r'\omega',
    'cdots': r'\cdots',

    # 폰트 명령어는 구조성 없음
    'rm': r'\rm',
    'it': r'\it',
}

LATEX_TO_HANGUL_SYMBOL = {
    r'\alpha': 'alpha',
    r'\beta': 'beta',
    r'\gamma': 'gamma',
    r'\delta': 'delta',
    r'\epsilon': 'epsilon',
    r'\zeta': 'zeta',
    r'\eta': 'eta',
    r'\theta': 'theta',
    r'\iota': 'iota',
    r'\kappa': 'kappa',
    r'\lambda': 'lambda',
    r'\mu': 'mu',
    r'\nu': 'nu',
    r'\xi': 'xi',
    r'o': 'omicron',
    r'\pi': 'pi',
    r'\rho': 'rho',
    r'\sigma': 'sigma',
    r'\tau': 'tau',
    r'\upsilon': 'upsilon',
    r'\phi': 'phi',
    r'\chi': 'chi',
    r'\psi': 'psi',
    r'\omega': 'omega',
    r'\cdots': 'cdots',

    r'\rm': 'rm',
    r'\it': 'it',
}