# converter/util/exceptions.py

class FormulaParseError(Exception):
    def __init__(self, message: str, token: str = None):
        detail = f" [Token: {token}]" if token else ""
        super().__init__(f"[FormulaParseError] {message}{detail}")