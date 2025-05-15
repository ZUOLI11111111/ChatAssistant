import os
import uvicorn
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取环境变量配置或使用默认值
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))
debug = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

if __name__ == "__main__":
    print(f"启动学习辅助AI Agent服务...")
    print(f"API文档将在 http://{host if host != '0.0.0.0' else 'localhost'}:{port}/docs 可用")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug
    ) 