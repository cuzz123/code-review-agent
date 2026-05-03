from app.workers import check_architecture, check_security, check_performance, check_style
from app.models import ReviewIssue, ReviewReport
from app.tools.code_analyzer import analyze_structure

def run_review(code: str, filename: str) -> ReviewReport:
    """运行完整代码审查"""
    # 1. 代码结构分析
    stats = analyze_structure(code, "python")

    # 2. 并发执行 4 个 Worker
    all_issues = []
    for worker in [check_architecture, check_security, check_performance, check_style]:
        raw_issues = worker(code, filename)
        for item in raw_issues:
            all_issues.append(ReviewIssue(
                severity=_normalize_severity(item.get("severity", "info")),
                category=_detect_category(worker.__name__),
                file=filename,
                title=item.get("title", ""),
                description=item.get("description", ""),
                suggestion=item.get("suggestion", ""),
            ))

    # 3. 计算评分
    score = _calculate_score(all_issues)

    # 4. 提取优点和建议
    strengths = _extract_strengths(stats)
    suggestions = [i.suggestion for i in all_issues[:5]]

    return ReviewReport(
        summary=f"审查完成：发现 {len(all_issues)} 个问题，评分 {score}/100",
        score=score,
        issues=all_issues,
        strengths=strengths,
        suggestions=suggestions,
    )

def _detect_category(worker_name: str) -> str:
    mapping = {
        "check_architecture": "architecture",
        "check_security": "security",
        "check_performance": "performance",
        "check_style": "style",
    }
    return mapping.get(worker_name, "architecture")

def _calculate_score(issues: str) -> int:
    score = 100
    for i in issues:
        if i.severity in ("critical", "CRITICAL", "high", "HIGH"):
            score -= 15
        elif i.severity in ("major", "MAJOR", "medium", "MEDIUM"):
            score -= 8
        elif i.severity in ("minor", "MINOR", "low", "LOW"):
            score -= 3
    return max(score, 0)

def _extract_strengths(stats: dict) -> list:
    s = []
    if stats["functions"]:
        s.append(f"定义了 {len(stats['functions'])} 个函数")
    if stats["classes"]:
        s.append(f"使用了面向对象设计，定义了 {len(stats['classes'])} 个类")
    if stats["total_lines"] < 500:
        s.append("代码规模适中，易于维护")
    return s

def _normalize_severity(s: str) -> str:
    """将 LLM 返回的严重级别映射到标准值"""
    mapping = {
        "critical": "critical", "CRITICAL": "critical",
        "high": "major", "HIGH": "major",
        "medium": "minor", "MEDIUM": "minor",
        "major": "major", "MAJOR": "major",
        "minor": "minor", "MINOR": "minor",
        "low": "info", "LOW": "info",
        "info": "info", "INFO": "info",
        "error": "major", "ERROR": "major",
        "warning": "minor", "WARNING": "minor",
    }
    return mapping.get(s.strip(), "info")