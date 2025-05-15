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
    try:
        # 构建提示信息
        prompt = f"科目: {request.subject}\n"
        prompt += f"年级: {request.grade_level or '未指定'}\n"
        prompt += f"问题: {request.question}\n"
        
        if request.additional_info:
            prompt += f"补充信息: {request.additional_info}\n"
            
        # 获取AI回答
        response = await get_ai_response(
            prompt=prompt,
            system_prompt="你是一个专业的作业辅导老师，请详细解答学生的问题，给出思路和解题步骤。"
        )
        
        return {
            "status": "success",
            "data": {
                "answer": response,
                "subject": request.subject,
                "question": request.question
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"作业辅导服务出错: {str(e)}")

@router.post("/explain")
async def explain_concept(
    subject: str = Body(..., embed=True),
    concept: str = Body(..., embed=True),
    depth: str = Body("medium", embed=True)
) -> Dict[str, Any]:
    """
    作业辅导功能 - 解释学科概念
    """
    try:
        depth_mapping = {
            "basic": "基础",
            "medium": "中等",
            "advanced": "高级"
        }
        
        depth_level = depth_mapping.get(depth, "中等")
        
        prompt = f"请以{depth_level}难度解释{subject}学科中的'{concept}'概念"
        
        response = await get_ai_response(
            prompt=prompt,
            system_prompt="你是一个专业的学科老师，擅长用清晰易懂的方式解释概念。"
        )
        
        return {
            "status": "success",
            "data": {
                "explanation": response,
                "subject": subject,
                "concept": concept,
                "depth": depth
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"概念解释服务出错: {str(e)}") 