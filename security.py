#security.py
import re

def sanitize_string(input_str: str) -> str:
    
    return re.sub(r"[;|$\b]", "", input_str)
