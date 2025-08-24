from fastapi import APIRouter, HTTPException, Body, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, HttpUrl

from app.services.crawler_service import crawl_article, summarize_content

router = APIRouter()

class CrawlRequest(BaseModel):
    url: HttpUrl
    extract_type: str = "full"  # full, summary, outline
    max_length: Optional[int] = None

@router.post("/article")
async def crawl_web_article(
    request: CrawlRequest
) -> Dict[str, Any]:
    """
    爬虫功能 - 爬取文章内容并处理
    """
    pass

@router.post("/video")
async def crawl_video_content(
    request: CrawlRequest
) -> Dict[str, Any]:
    """
    爬虫功能 - 爬取视频内容(字幕/描述)并处理
    """
    pass

@router.get("/search")
async def search_resources(
    query: str,
    resource_type: str = Query("all", description="资源类型: all, article, video"),
    limit: int = Query(5, ge=1, le=20, description="结果数量限制")
) -> Dict[str, Any]:
    """
    爬虫功能 - 搜索相关学习资源
    """
    pass