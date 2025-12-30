# Vercel Serverless API - 使用 HTTP handler 方式
from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import os
import io
import re
from typing import List, Optional
from urllib.parse import urlparse

app = FastAPI()

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
API_BASE_URL = "https://api.deepseek.com"

# 数据模型
class Message(BaseModel):
    role: str
    content: str

class DocumentContext(BaseModel):
    name: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    documentContexts: List[DocumentContext] = []

class CrawlRequest(BaseModel):
    url: str

# 文档解析函数
def extract_text_from_pdf(file_content: bytes) -> str:
    """从 PDF 文件提取文本"""
    try:
        import PyPDF2
        pdf_file = io.BytesIO(file_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF解析失败: {str(e)}")

def extract_text_from_txt(file_content: bytes) -> str:
    """从 TXT 文件提取文本"""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file_content.decode('gbk')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"文本文件解析失败: {str(e)}")

# API endpoints
@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "api_configured": bool(DEEPSEEK_API_KEY),
        "message": "Vercel Serverless API is running"
    }

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """文件上传处理"""
    try:
        # 读取文件内容
        content = await file.read()
        
        # 检查文件大小 (限制为 4.5MB，因为 Vercel 有 5MB 限制)
        if len(content) > 4.5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="文件大小超过限制 (最大 4.5MB)")
        
        # 根据文件类型提取文本
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="不支持的文件类型，仅支持 PDF 和 TXT")
        
        return {
            "success": True,
            "filename": file.filename,
            "content": text[:10000]  # 限制返回内容长度
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@app.post("/api/crawl")
async def crawl_webpage(request: CrawlRequest):
    """网页爬取"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(request.url)
            response.raise_for_status()
            
            # 简单提取文本（移除 HTML 标签）
            html_content = response.text
            text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            return {
                "success": True,
                "url": request.url,
                "content": text[:10000]  # 限制返回内容长度
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"网页爬取失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天对话 - 流式输出"""
    from fastapi.responses import StreamingResponse
    
    if not DEEPSEEK_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API密钥未配置，请在 Vercel 环境变量中设置 DEEPSEEK_API_KEY"
        )
    
    async def generate_stream():
        try:
            # 构建消息历史
            messages = []
            
            # 添加系统提示语和文档上下文
            if request.documentContexts:
                system_content = """你是Axon，由Axon开发组开发的专业AI研究助手。请基于用户上传的文档内容提供结构化、清晰的回答。

## 身份信息：
- 名称：Axon
- 开发者：Axon开发组
- 定位：专业的AI研究助手，擅长文档分析、知识管理和研究辅助

## 回答格式要求：
1. 使用Markdown格式组织内容，包括标题、列表、段落等
2. 对于复杂回答，使用标题层级（# ## ###）进行分段
3. 重要信息使用**粗体**强调
4. 数学公式使用LaTeX格式（行内：$...$，独立：$$...$$）
5. 代码使用```语言标记进行代码块包裹
6. 使用列表（- 或 1.）组织要点
7. 适当使用分段，提高可读性

文档内容:

"""
                for idx, doc in enumerate(request.documentContexts, 1):
                    system_content += f"--- 文档 {idx}: {doc.name} ---\n"
                    system_content += f"{doc.content[:2000]}\n\n"
                
                messages.append({
                    "role": "system",
                    "content": system_content
                })
            else:
                # 默认系统消息（无文档时）
                messages.append({
                    "role": "system",
                    "content": """你是Axon，由Axon开发组开发的专业AI研究助手。

## 身份信息：
- 名称：Axon
- 开发者：Axon开发组
- 定位：专业的AI研究助手，擅长文档分析、知识管理和研究辅助

## 回答格式要求：
1. 使用Markdown格式组织内容，提供清晰的结构
2. 对复杂问题使用标题分段（# ## ###）
3. 重要概念用**粗体**强调
4. 数学公式用LaTeX格式（$...$或$$...$$）
5. 代码用```语言标记包裹
6. 用列表组织要点（- 或 1.）
7. 适当分段，让回答易读易懂

请提供准确、结构化、专业的回答。"""
                })
            
            # 添加历史对话
            for msg in request.history:
                messages.append({"role": msg.role, "content": msg.content})
            
            # 添加当前消息
            messages.append({"role": "user", "content": request.message})
            
            # 调用 DeepSeek API（流式）
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    f"{API_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2000,
                        "stream": True
                    }
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        yield f"data: {{\"error\": \"API错误: {error_text.decode()}\"}}\n\n"
                        return
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str.strip() == "[DONE]":
                                yield f"data: {{\"done\": true}}\n\n"
                                break
                            
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        # 转义内容中的引号和换行符
                                        content_escaped = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                                        yield f"data: {{\"content\": \"{content_escaped}\"}}\n\n"
                            except json.JSONDecodeError:
                                continue
        
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/event-stream")

# 其他功能在 Vercel 上不可用
@app.post("/api/audio-to-text")
async def audio_to_text(file: UploadFile = File(...)):
    """音频转文字 - Vercel不支持"""
    raise HTTPException(
        status_code=501,
        detail="音频转文字功能在 Vercel 上不可用，需要服务器环境"
    )

@app.post("/api/generate-mindmap")
async def generate_mindmap(request: dict):
    """思维导图生成 - Vercel不支持"""
    raise HTTPException(
        status_code=501,
        detail="思维导图生成功能在 Vercel 上不可用，需要服务器环境"
    )

@app.post("/api/data-analysis")
async def data_analysis(request: dict):
    """数据分析 - Vercel不支持"""
    raise HTTPException(
        status_code=501,
        detail="数据分析功能在 Vercel 上不可用，需要服务器环境"
    )

@app.post("/api/generate-quiz")
async def generate_quiz(request: dict):
    """测验生成 - Vercel不支持"""
    raise HTTPException(
        status_code=501,
        detail="测验生成功能在 Vercel 上不可用，需要服务器环境"
    )
