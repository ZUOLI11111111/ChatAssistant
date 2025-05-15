from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.services.ai_service import get_ai_response

router = APIRouter()

class HomeworkQuestion(BaseModel):
    subject: str
    question: str
    grade_level: Optional[str] = None
    additional_info: Optional[str] = None

@router.post("/ask")
async def ask_homework_question(
    request: HomeworkQuestion
) -> Dict[str, Any]:
    """
    作业辅导功能 - 回答学生的作业问题
    """
    pass

@router.post("/explain")
async def explain_concept(
    subject: str = Body(..., embed=True),
    concept: str = Body(..., embed=True),
    depth: str = Body("medium", embed=True)
) -> Dict[str, Any]:
    """
    作业辅导功能 - 解释学科概念
    """
    pass
