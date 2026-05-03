import re
from typing import Dict

def analyze_structure(code: str, language: str) -> Dict:
    """分析代码结构"""
    result = {
        "total_lines": len(code.split("\n")),
        "blank_lines": 0,
        "comment_lines": 0,
        "functions": [],
        "classes": [],
        "imports": [],
    }

    for line in code.split("\n"):
        stripped = line.strip()
        if not stripped:
            result["blank_lines"] += 1
        elif stripped.startswith(('#', '//', '/', "")):
            result["comment_lines"] += 1

    # 提取 Python 函数和类
    if language == "python":
        result["functions"] = re.findall(r"^def (\w+)\(", code, re.MULTILINE)
        result["classes"] = re.findall(r"^class (\w+)", code, re.MULTILINE)
        result["imports"] = re.findall(r"^(?:import|from)\s+(\S+)", code, re.MULTILINE)

    return result
    