# converter/mapping/map.py

# 한글 → LaTeX 변환 맵
HANGUL_TO_LATEX = {
    # 지수
    '^': r'^',

    # 루트
    'root': r'\sqrt',

    # 로그
    'log': r'\log',

    # 삼각함수
    'sin': r'\sin',
    'cos': r'\cos',
    'tan': r'\tan',

    # 분수
    'frac': r'\frac',

    # 조합
    'binom': r'\binom',

    # 적분
    'integral': r'\int',

    # 극한
    'lim': r'\lim',

    # 이항 연산자
    'times': r'\times',
    'div': r'\div',
    'ge': r'\geq',
    'le': r'\leq',
    'ne': r'\neq',

    # 괄호
    'LEFT': r'\LEFT',
    'RIGHT': r'\RIGHT',

    # 부등호
    'not' : r'\ne'
}

# LaTeX → 한글 변환 맵
LATEX_TO_HANGUL = {
    # 루트
    r'\sqrt': 'root',

    # 로그
    r'\log': 'log',

    # 삼각함수
    r'\sin': 'sin',
    r'\cos': 'cos',
    r'\tan': 'tan',

    # 분수
    r'\frac': 'frac',

    # 조합
    r'\binom': 'binom',

    # 적분
    r'\int': 'integral',

    # 극한
    r'\lim': 'lim',

    # 이항 연산자
    r'\times': 'times',
    r'\div': 'div',
    r'\geq': 'ge',
    r'\leq': 'le',
    r'\neq': 'ne',

    # 괄호
    r'\LEFT': 'LEFT',
    r'\RIGHT': 'RIGHT',

    # 부등호
    r'\ne' : 'not'

}