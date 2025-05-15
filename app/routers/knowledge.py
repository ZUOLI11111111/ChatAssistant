from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from app.services.ai_service import get_ai_response

router = APIRouter()

class KnowledgeQuestion(BaseModel):
    question: str
    context: Optional[str] = None
    topics: Optional[List[str]] = None

@router.post("/ask")
async def ask_knowledge_question(
    request: KnowledgeQuestion
) -> Dict[str, Any]:
    

@router.post("/upload")
async def process_document(
    file: UploadFile = File(...),
    question: str = Form(...)
) -> Dict[str, Any]:
    

@router.post("/compare")
async def compare_concepts(
    concept1: str = Form(...),
    concept2: str = Form(...),
    subject: Optional[str] = Form(None)
) -> Dict[str, Any]:
   