import re

def sanitize_string(input: str) -> str:
    return re.sub(r"[^a-zA-Z0-9 \\-]" ,"", input)
