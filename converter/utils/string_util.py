# converter/utils/string_util.py

def to_pascal_case(snake_str: str) -> str:
    parts = snake_str.lower().split('_')
    return ''.join(word.capitalize() for word in parts)