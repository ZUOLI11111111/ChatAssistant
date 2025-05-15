import os
from typing import Optional, Dict, Any, List
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_ai_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
   

# 用于知识库问答的函数
async def query_with_context(
    question: str,
    context: str,
    system_prompt: Optional[str] = None
) -> str:
   
   
  

# 格式化输出的函数
async def format_response(
    content: str,
    format_type: str = "paragraph",
    language: str = "chinese"
) -> str:
    
    