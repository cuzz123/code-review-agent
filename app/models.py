from pydantic import BaseModel
from typing import List, Optional, Literal

class CodeFile(BaseModel):
    """单个代码文件"""
    path: str
    content: str
    language: str = "unknown"

class ReviewRequest(BaseModel):
    """审查请求"""
    code: Optional[str] = None
    language: Optional[str] = None
    github_url: Optional[str] = None
    files: Optional[List[CodeFile]] = None

class ReviewIssue(BaseModel):
    """审查发现的问题"""
    severity: Literal["critical", "major", "minor", "info"]
    category: Literal["architecture", "security", "performance", "style"]
    file: str
    line: Optional[int] = None
    title: str
    description: str
    suggestion: str

class ReviewReport(BaseModel):
    """审查报告"""
    summary: str
    score: int # 0-100
    issues: List[ReviewIssue]
    strengths: List[str]
    suggestions: List[str]