# converter/lookup/latex_lookup.py

from functools import lru_cache

import converter.mapping.map as map  # 맵 딕셔너리들 들어있는 파일

def get_all_latex_to_hangul_maps():
    return {
        name: obj for name, obj in vars(map).items()
        if name.startswith("LATEX_TO_HANGUL_") and isinstance(obj, dict)
    }

@lru_cache(maxsize=None) # 토큰이 들어올 때마다 딕셔너리 전부 순회 -> 캐시로 개선 - 현재는 딕셔너리가 작고 단순해서 큰 이득이 없음
def get_hangul_token_from_latex(token: str) -> str:
    for name, mapping in vars(map).items():
        if name.startswith("LATEX_TO_HANGUL_") and isinstance(mapping, dict):
            if token in mapping:
                print(f"[DEBUG] '{token}' → '{mapping[token]}' (from {name})")
                return mapping[token]
    print(f"[DEBUG] '{token}' not found in any LATEX_TO_HANGUL_* map")
    return token