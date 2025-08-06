# 学习辅助AI Agent

基于FastAPI构建的学习辅助AI代理系统，提供作业辅导、知识答疑和内容爬虫功能。

## 功能特点

1. **作业辅导助手**
   - 解答各学科作业问题
   - 提供详细的解题思路和步骤
   - 解释学科概念和知识点

2. **知识答疑**
   - 回答一般知识问题
   - 基于上传文档回答问题
   - 比较不同概念的异同点

3. **内容爬虫**
   - 爬取并处理网络文章
   - 提取视频内容和摘要
   - 搜索相关学习资源

## 技术栈

- **后端**: FastAPI, Python 3.12 venv
- **AI服务**: deepseek API
- **内容处理**: BeautifulSoup4, Requests
- **异步处理**: asyncio

## 快速开始

### 环境准备

1. 克隆项目并进入项目目录
   ```bash
   git clone https://github.com/ZUOLI11111111/ChatAssistant.git
   cd ChatAssistant
   ```

2. 创建虚拟环境并安装依赖 操作系统:WSL UBUNTU24
   ```bash
   python -m venv venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 配置环境变量
   ```bash
   在app/config/config.toml
   ```

### 启动服务（暂时不需要）

```bash
uvicorn app.main:app --reload
```

服务将在 http://localhost:8000 启动，API文档可通过 http://localhost:8000/docs 访问。

## API接口

### 作业辅导

- `POST /api/homework/ask`: 提交作业问题
- `POST /api/homework/explain`: 解释学科概念

### 知识答疑

- `POST /api/knowledge/ask`: 提问一般知识问题
- `POST /api/knowledge/upload`: 上传文档并提问
- `POST /api/knowledge/compare`: 比较两个概念的异同

### 内容爬虫

- `POST /api/crawler/article`: 爬取文章内容
- `POST /api/crawler/video`: 爬取视频内容
- `GET /api/crawler/search`: 搜索学习资源

## 项目结构

```
study-assistant-ai/
├── app/
│   ├── main.py           # 主应用入口
│   ├── routers/          # API路由
│   │   ├── homework.py   # 作业辅导路由
│   │   ├── knowledge.py  # 知识答疑路由
│   │   └── crawler.py    # 内容爬虫路由
│   ├── models/           # 数据模型
│   ├── services/         # 服务层
│   │   ├── ai_service.py    # AI服务接口
│   │   └── crawler_service.py # 爬虫服务
│   └── utils/            # 工具函数
├── .env                  # 环境变量
├── requirements.txt      # 项目依赖
└── README.md             # 项目说明
```

## 注意事项

- 本项目需要OpenAI API密钥才能正常运行
- 爬虫功能仅用于学习目的，请遵守相关网站的使用条款
- 实际部署时请调整CORS和安全设置

## 许可证

[MIT](LICENSE)
