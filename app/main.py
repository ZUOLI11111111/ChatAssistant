import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import homework, knowledge, crawler

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="学习辅助AI Agent",
    description="提供作业辅导、知识答疑和内容爬虫功能的API",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(homework.router, prefix="/api/homework", tags=["作业辅导"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识答疑"])
app.include_router(crawler.router, prefix="/api/crawler", tags=["内容爬虫"])

@app.get("/")
async def root():
    return {"message": "欢迎使用学习辅助AI Agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
