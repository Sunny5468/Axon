# Vercel Serverless API - 完整版
from fastapi import FastAPI, HTTPException, UploadFile, File
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
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")

def extract_text_from_txt(file_content: bytes) -> str:
    """从文本文件提取文本"""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file_content.decode('gbk')
        except:
            raise Exception("文本文件编码不支持")

def extract_text_from_html(html: str) -> str:
    """从 HTML 中提取纯文本"""
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# API 端点
@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "message": "Axon API is running on Vercel",
        "api_configured": bool(DEEPSEEK_API_KEY)
    }

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传并解析文档 (限制: 4.5MB)"""
    try:
        content = await file.read()
        
        # 检查文件大小 (Vercel 限制 4.5MB)
        if len(content) > 4.5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="文件过大，Vercel限制为4.5MB")
        
        filename = file.filename.lower()
        
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif filename.endswith('.txt') or filename.endswith('.md'):
            text = extract_text_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="仅支持 PDF 和 TXT 文件")
        
        return {
            "status": "success",
            "filename": file.filename,
            "content": text[:5000],
            "length": len(text),
            "message": f"成功解析文档，共 {len(text)} 字符"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档解析失败: {str(e)}")

@app.post("/api/crawl")
async def crawl_webpage(request: CrawlRequest):
    """爬取网页内容"""
    try:
        url = request.url.strip()
        parsed_url = urlparse(url)
        
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="无效的URL格式")
        
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, 
                                  detail=f"无法访问网页: HTTP {response.status_code}")
            
            text_content = extract_text_from_html(response.text)
            
            if not text_content or len(text_content.strip()) < 10:
                raise HTTPException(status_code=400, detail="网页内容为空或无法解析")
            
            domain = parsed_url.netloc.replace('www.', '')
            filename = f"网页_{domain}"
            
            return {
                "status": "success",
                "filename": filename,
                "content": text_content[:5000],
                "length": len(text_content),
                "url": url,
                "message": f"成功爬取网页，共 {len(text_content)} 字符"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"爬取失败: {str(e)}")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天接口"""
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="API密钥未配置")
    
    messages = []
    
    if request.documentContexts:
        context_text = "\n\n".join([
            f"文档【{doc.name}】:\n{doc.content[:2000]}"
            for doc in request.documentContexts
        ])
        messages.append({
            "role": "system",
            "content": f"你是Axon AI助手。参考文档:\n\n{context_text}"
        })
    
    for msg in request.history[-10:]:
        messages.append({"role": msg.role, "content": msg.content})
    
    messages.append({"role": "user", "content": request.message})
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="API调用失败")
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return {"content": content, "done": True}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-audio-summary")
async def generate_audio_summary(request: dict):
    """音频生成 - Vercel不支持"""
    raise HTTPException(
        status_code=501,
        detail="音频生成功能在 Vercel 上不可用，需要服务器环境"
    )

@app.post("/api/generate-mindmap")
async def generate_mindmap(request: dict):
    """思维导图生成 - Vercel不支持"""
    raise HTTPException(
        status_code=501,
        detail="思维导图生成功能在 Vercel 上不可用，需要服务器环境"
    )

@app.post("/api/analyze-data")
async def analyze_data(request: dict):
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
