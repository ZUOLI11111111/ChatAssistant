from fastapi import APIRouter, HTTPException, Body, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, HttpUrl

from app.services.crawler_service import crawl_article, crawl_video, summarize_content

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
    try:
        content = await crawl_article(str(request.url))
        
        if request.extract_type != "full":
            content = await summarize_content(
                content=content, 
                extract_type=request.extract_type,
                max_length=request.max_length
            )
        
        return {
            "status": "success",
            "data": {
                "url": str(request.url),
                "content": content,
                "extract_type": request.extract_type
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文章爬取服务出错: {str(e)}")

@router.post("/video")
async def crawl_video_content(
    request: CrawlRequest
) -> Dict[str, Any]:
    """
    爬虫功能 - 爬取视频内容(字幕/描述)并处理
    """
    try:
        content = await crawl_video(str(request.url))
        
        if request.extract_type != "full":
            content = await summarize_content(
                content=content, 
                extract_type=request.extract_type,
                max_length=request.max_length
            )
        
        return {
            "status": "success",
            "data": {
                "url": str(request.url),
                "content": content,
                "extract_type": request.extract_type
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"视频爬取服务出错: {str(e)}")

@router.get("/search")
async def search_resources(
    query: str,
    resource_type: str = Query("all", description="资源类型: all, article, video"),
    limit: int = Query(5, ge=1, le=20, description="结果数量限制")
) -> Dict[str, Any]:
    """
    爬虫功能 - 搜索相关学习资源
    """
    try:
        # 这里应该实现一个搜索引擎API或自定义爬虫逻辑
        # 简化起见，此处返回示例数据
        
        results = [
            {
                "title": f"关于{query}的学习资源 {i+1}",
                "url": f"https://example.com/resource/{i+1}",
                "type": "article" if i % 2 == 0 else "video",
                "description": f"这是关于{query}的一个示例资源描述"
            }
            for i in range(limit)
        ]
        
        # 如果指定了资源类型且不是"all"，则过滤结果
        if resource_type != "all":
            results = [r for r in results if r["type"] == resource_type]
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "resource_type": resource_type,
                "results": results,
                "total": len(results)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"资源搜索服务出错: {str(e)}") 