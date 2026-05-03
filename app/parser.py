from app.models import CodeFile

LANGUAGE_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".java": "java", ".go": "go", ".rs": "rust",
    ".cpp": "cpp", ".c": "c", ".h": "cpp",
    ".html": "html", ".css": "css", ".json": "json",
    ".yaml": "yaml", ".yml": "yaml", ".md": "markdown",
    ".sql": "sql", ".sh": "bash", ".rb": "ruby",
}

def detect_language(filename: str, code: str = "") -> str:
    """根据文件名后缀或代码内容判断语言"""
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
    ext = f".{ext}"
    if ext in LANGUAGE_MAP:
        return LANGUAGE_MAP[ext]
    # 用内容简单判断
    if code.strip().startswith(("import ", "from ", "def ", "class ")):
        return "python"
    return "unknown"

def parse_code(filename: str, code: str) -> CodeFile:
    """解析代码文件"""
    language = detect_language(filename, code)
    return CodeFile(path=filename, content=code, language=language)