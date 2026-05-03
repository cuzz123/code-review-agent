from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import ReviewRequest, ReviewReport
from app.supervisor import run_review

app = FastAPI(title="AI Code Review Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/review")
def review_code(req: ReviewRequest) -> ReviewReport:
    """提交代码审查"""
    if not req.code:
        return ReviewReport(
            summary="请提供需要审查的代码",
            score=0,
            issues=[],
            strengths=[],
            suggestions=[],
        )
    return run_review(req.code, req.language or "source.py")


@app.get("/health")
def health():
    return {"status": "ok"}
