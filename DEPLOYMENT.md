# NotebookLLM 部署指南

## 🚀 快速部署

### Windows用户

#### 方案1：使用批处理文件（最简单）

1. **后端启动**
   - 双击运行 `run_backend.bat`
   - 等待显示 "Backend is starting on http://localhost:8000"

2. **前端启动**（新建命令行窗口）
   - 双击运行 `run_frontend.bat`
   - 浏览器自动打开 `http://localhost:3000`

#### 方案2：手动启动

**启动后端：**
```powershell
cd backend
pip install -r requirements.txt
python main.py
```

**启动前端：**（新建PowerShell窗口）
```powershell
cd frontend
python -m http.server 3000
```

然后在浏览器打开：`http://localhost:3000`

### macOS/Linux用户

```bash
# 给脚本执行权限
chmod +x run_backend.sh
chmod +x run_frontend.sh

# 启动后端（终端1）
./run_backend.sh

# 启动前端（终端2）
./run_frontend.sh
```

## 📦 安装依赖

### 后端依赖安装

```bash
cd backend
pip install -r requirements.txt
```

**依赖说明：**
- `fastapi` - 高性能Web框架
- `uvicorn` - ASGI服务器
- `httpx` - 异步HTTP客户端（调用LLM API）
- `pydantic` - 数据验证和设置管理

### 前端

纯HTML+CSS+JavaScript，无需安装额外依赖！

## 🔑 配置API密钥

### 方法1：环境变量（推荐）

**Windows PowerShell：**
```powershell
$env:OPENAI_API_KEY = "sk-5610a05204284964a0953677a117a9dd"
python main.py
```

**Windows CMD：**
```cmd
set OPENAI_API_KEY=sk-5610a05204284964a0953677a117a9dd
python main.py
```

**macOS/Linux：**
```bash
export OPENAI_API_KEY="sk-5610a05204284964a0953677a117a9dd"
python main.py
```

### 方法2：创建.env文件

在 `backend` 目录创建 `.env` 文件：

```
OPENAI_API_KEY=sk-5610a05204284964a0953677a117a9dd
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx  # 如果使用Claude
```

然后修改 `main.py`：

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
}
```

### 方法3：直接修改代码

编辑 `backend/main.py`：

```python
API_KEYS = {
    "openai": "sk-5610a05204284964a0953677a117a9dd",
    "anthropic": "",  # 留空如果不使用
}
```

## ✅ 验证安装

### 检查后端

打开浏览器访问：
- `http://localhost:8000` - API主页
- `http://localhost:8000/health` - 健康检查
- `http://localhost:8000/docs` - 交互式API文档（Swagger UI）

### 检查前端

访问：`http://localhost:3000`

应该看到一个紫色背景的NotebookLLM界面。

## 🧪 测试API

### 使用curl测试生成讨论

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的机器。",
    "depth": "medium",
    "length": "short",
    "tone": "professional",
    "speaker1": "张教授",
    "speaker2": "李学生"
  }'
```

### 使用Python测试

```python
import requests

url = "http://localhost:8000/api/generate"
data = {
    "content": "Python是一种高级编程语言...",
    "depth": "medium",
    "length": "short",
    "tone": "casual",
    "speaker1": "小王",
    "speaker2": "小李"
}

response = requests.post(url, json=data)
print(response.json())
```

## 🔧 常见问题

### Q: 启动后端时报错"Address already in use"

**A:** 8000端口已被占用
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# 或者改用其他端口
uvicorn main:app --port 8001
```

### Q: "No module named 'fastapi'"

**A:** 没有安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### Q: API返回"401 Unauthorized"

**A:** API密钥无效或过期
- 验证密钥 `sk-5610a05204284964a0953677a117a9dd`
- 检查OpenAI账户是否有余额
- 确认环境变量设置正确

### Q: 生成速度很慢

**A:** 可能的原因和解决方案
- 使用GPT-3.5-turbo而不是GPT-4（更快）
- 减少对话长度设置
- 检查网络连接
- 尝试在非高峰时间运行

### Q: 前端无法连接后端

**A:** CORS问题或后端未运行
```javascript
// 在前端检查
console.log('后端URL:', 'http://localhost:8000');

// 后端已启用CORS，确保访问正确的URL
```

## 🐳 Docker部署（可选）

创建 `Dockerfile`：

```dockerfile
FROM python:3.10

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
docker build -t notebookllm-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY="sk-xxxx" notebookllm-backend
```

## 📊 生产环境建议

### 1. 使用环境变量

```python
import os
from typing import Dict

API_KEYS: Dict[str, str] = {
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
}

if not API_KEYS["openai"]:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

### 2. 添加速率限制

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/generate")
@limiter.limit("10/minute")
async def generate_discussion(request: GenerateRequest):
    ...
```

### 3. 添加请求日志

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/generate")
async def generate_discussion(request: GenerateRequest):
    logger.info(f"生成讨论: {request.speaker1} vs {request.speaker2}")
    ...
```

### 4. 使用HTTPS

```bash
pip install python-multipart
```

配置Nginx反向代理或使用Let's Encrypt证书。

## 🚢 部署到云服务

### Heroku

```bash
# 创建Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 部署
heroku login
heroku create notebookllm-api
git push heroku main
```

### AWS EC2

```bash
# 安装Python和依赖
sudo apt-get update
sudo apt-get install python3-pip
pip3 install -r requirements.txt

# 使用PM2保持服务运行
npm install -g pm2
pm2 start "python main.py" --name notebookllm
pm2 startup
```

### Google Cloud Run

```bash
# 创建.gcloudignore
# 部署
gcloud run deploy notebookllm --source .
```

## 📞 获取帮助

- 查看API文档: `http://localhost:8000/docs`
- 检查日志: 查看终端输出
- 提交Issue: GitHub repository
