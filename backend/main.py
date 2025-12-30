from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
import json
import random
import os
from typing import List
import PyPDF2
import docx
import io
import asyncio
from urllib.parse import urlparse
import re

# 加载环境变量（开发环境）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # 生产环境可能没有 python-dotenv

app = FastAPI()

# CORS配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建音频存储目录
AUDIO_DIR = os.path.join(BASE_DIR, "audio_files")
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# 创建图表存储目录
DIAGRAM_DIR = os.path.join(BASE_DIR, "diagram_files")
if not os.path.exists(DIAGRAM_DIR):
    os.makedirs(DIAGRAM_DIR)

# Frontend目录
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# 挂载静态文件目录
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")
app.mount("/diagrams", StaticFiles(directory=DIAGRAM_DIR), name="diagrams")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

# DeepSeek API配置 - 从环境变量读取
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")  # 从环境变量获取API密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_REASONER_MODEL = "deepseek-reasoner"  # 用于思维导图生成

# 演示模式 (当API密钥无效时使用)
DEMO_MODE = not DEEPSEEK_API_KEY  # 如果没有配置API密钥，自动启用演示模式

# 文档解析函数
def extract_text_from_pdf(file_content: bytes) -> str:
    """从 PDF 文件提取文本"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")

def extract_text_from_docx(file_content: bytes) -> str:
    """从 Word 文件提取文本"""
    try:
        docx_file = io.BytesIO(file_content)
        doc = docx.Document(docx_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Word文档解析失败: {str(e)}")

def extract_text_from_txt(file_content: bytes) -> str:
    """从文本文件提取文本"""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file_content.decode('gbk')
        except:
            raise Exception("文本文件编码不支持")

class DocumentContext(BaseModel):
    name: str
    content: str

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    documentContexts: List[DocumentContext] = []

class CrawlRequest(BaseModel):
    url: str

class AudioSummaryRequest(BaseModel):
    conversation: List[Message]

class MindMapRequest(BaseModel):
    conversation: List[Message]

class DataAnalysisRequest(BaseModel):
    documents: List[DocumentContext]

class QuizRequest(BaseModel):
    documents: List[DocumentContext]

@app.get("/")
async def read_root():
    """返回前端页面"""
    frontend_path = os.path.join(BASE_DIR, "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "NotebookLLM API with DeepSeek", "status": "running", "mode": "DEMO" if DEMO_MODE else "PRODUCTION"}

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "message": "NotebookLLM Backend is running", "mode": "DEMO" if DEMO_MODE else "PRODUCTION"}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    上传并解析文档
    支持格式: PDF, Word (.doc, .docx), TXT, MD
    """
    try:
        # 读取文件内容
        content = await file.read()
        filename = file.filename.lower()
        
        # 根据文件类型解析
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            text = extract_text_from_docx(content)
        elif filename.endswith('.txt') or filename.endswith('.md'):
            text = extract_text_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        return {
            "status": "success",
            "filename": file.filename,
            "content": text[:5000],  # 返回前5000字符预览
            "length": len(text),
            "message": f"成功解析文档，共 {len(text)} 字符"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档解析失败: {str(e)}")

@app.post("/api/crawl")
async def crawl_webpage(request: CrawlRequest):
    """
    爬取网页内容
    """
    try:
        url = request.url.strip()
        
        # 验证URL格式
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="无效的URL格式")
        
        # 获取网页内容
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, 
                                  detail=f"无法访问网页: HTTP {response.status_code}")
            
            # 提取文本内容
            html_content = response.text
            text_content = extract_text_from_html(html_content)
            
            if not text_content or len(text_content.strip()) < 10:
                raise HTTPException(status_code=400, detail="网页内容为空或无法解析")
            
            # 生成文件名
            domain = parsed_url.netloc.replace('www.', '')
            filename = f"自动爬取_{domain}"
            
            return {
                "status": "success",
                "filename": filename,
                "content": text_content[:5000],  # 返回前5000字符预览
                "length": len(text_content),
                "url": url,
                "message": f"成功爬取网页，共 {len(text_content)} 字符"
            }
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="请求超时，请检查网络或网址")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"爬取失败: {str(e)}")

def extract_text_from_html(html: str) -> str:
    """
    从 HTML 中提取纯文本内容（简单方法）
    """
    # 移除script和style标签
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # 解码HTML实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # 清理多余空格和换行
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    聊天接口 - 使用DeepSeek API (流式输出)
    
    参数:
    - message: 用户的消息
    - history: 对话历史记录
    - documentContexts: 文档上下文
    """
    
    try:
        # 构建消息列表
        messages = []
        
        # 如果有文档内容，添加系统消息
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
                system_content += f"{doc.content[:3000]}\n\n"  # 限制每个文档最多3000字符
            
            messages.append({
                "role": "system",
                "content": system_content
            })
        else:
            # 默认系统消息
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
        
        # 添加历史记录
        if request.history:
            for item in request.history:
                messages.append({
                    "role": item.role,
                    "content": item.content
                })
        
        # 添加当前消息
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # 演示模式
        if DEMO_MODE:
            async def demo_stream():
                demo_text = f"我收到了您的消息: \"{request.message}\"\n\n现在处于演示模式。数学公式示例: $E = mc^2$ 和 $$\\int_0^\\infty e^{{-x}} dx = 1$$"
                for char in demo_text:
                    yield f"data: {json.dumps({'content': char}, ensure_ascii=False)}\n\n"
                    await asyncio.sleep(0.02)
                yield f"data: {json.dumps({'done': True})}\n\n"
            
            return StreamingResponse(demo_stream(), media_type="text/event-stream")
        
        # 流式生成器
        async def generate_stream():
            try:
                async with httpx.AsyncClient() as client:
                    async with client.stream(
                        "POST",
                        DEEPSEEK_API_URL,
                        json={
                            "model": DEEPSEEK_MODEL,
                            "messages": messages,
                            "temperature": 0.7,
                            "top_p": 0.95,
                            "max_tokens": 2000,
                            "stream": True  # 启用流式输出
                        },
                        headers={
                            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        timeout=60.0
                    ) as response:
                        if response.status_code != 200:
                            error_text = await response.aread()
                            yield f"data: {json.dumps({'error': f'API error: {response.status_code}'})}\n\n"
                            return
                        
                        # 逐行读取流式响应
                        async for line in response.aiter_lines():
                            if line.strip():
                                if line.startswith("data: "):
                                    line = line[6:]  # 移除 "data: " 前缀
                                
                                if line.strip() == "[DONE]":
                                    yield f"data: {json.dumps({'done': True})}\n\n"
                                    break
                                
                                try:
                                    chunk_data = json.loads(line)
                                    if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                        delta = chunk_data["choices"][0].get("delta", {})
                                        content = delta.get("content", "")
                                        if content:
                                            yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
                                except json.JSONDecodeError:
                                    continue
                        
                        # 确保发送完成信号
                        yield f"data: {json.dumps({'done': True})}\n\n"
                        
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(generate_stream(), media_type="text/event-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/api/generate-audio-summary")
async def generate_audio_summary(request: AudioSummaryRequest):
    """
    生成对话音频总结
    """
    try:
        # 1. 使用LLM总结对话
        conversation_text = "\n".join([
            f"{msg.role}: {msg.content}" for msg in request.conversation
        ])
        
        summary_prompt = f"""请对以下对话进行简洁、清晰的总结，重点提取关键信息和结论。总结应该简洁易懂，适合语音播报：

{conversation_text}

请用中文回答，内容控制在200字以内。"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的对话总结助手。"},
                        {"role": "user", "content": summary_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM API error: {response.status_code}")
            
            data = response.json()
            summary = data["choices"][0]["message"]["content"].strip()
        
        # 2. 使用gTTS生成语音（简单免费方案）
        try:
            from gtts import gTTS
            import datetime
            
            # 生成文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"当前对话汇总_{timestamp}"
            audio_filename = f"{filename}.mp3"
            audio_path = os.path.join(AUDIO_DIR, audio_filename)
            
            # 生成语音
            tts = gTTS(text=summary, lang='zh-cn', slow=False)
            tts.save(audio_path)
            
            return {
                "status": "success",
                "filename": filename,
                "audio_url": f"/audio/{audio_filename}",
                "summary": summary,
                "message": "音频总结生成成功"
            }
            
        except ImportError:
            raise HTTPException(
                status_code=500, 
                detail="gTTS 未安装，请运行: pip install gTTS"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成音频总结失败: {str(e)}")

@app.post("/api/generate-mindmap")
async def generate_mindmap(request: MindMapRequest):
    """
    使用Reasoner模型生成Mermaid思维导图
    """
    try:
        # 1. 构建对话内容
        conversation_text = "\n\n".join([
            f"{msg.role.upper()}: {msg.content}" for msg in request.conversation[-10:]  # 只取最近10轮对话
        ])
        
        # 2. Mermaid生成提示词（优化版）
        mermaid_prompt = f"""请为以下对话内容生成一个专业、美观的Mermaid思维导图。

## 对话内容：
{conversation_text}

## Mermaid思维导图要求：
1. **语法**：使用mindmap语法
2. **结构**：
   - 中心主题清晰、简洁
   - 分支层次分明，2-4层为宜
   - 每个节点使用关键词和短语
3. **样式**：
   - 使用圆括号 ((主题)) 表示中心节点
   - 使用方括号 [重点内容] 突出关键分支
   - 使用 **粗体** 强调重要概念
4. **逻辑**：
   - 结构清晰、层次分明
   - 同级概念保持平衡
   - 体现内容的主次关系

## 输出格式：
```mermaid
mindmap
  root((中心主题))
    [主要分支1]
      子概念1.1
      子概念1.2
    [主要分支2]
      子概念2.1
        细节2.1.1
      子概念2.2
    分支3
      子概念3.1
```

**要求：请直接输出Mermaid代码，确保格式正确、内容完整。**
"""
        
        # 3. 使用Reasoner模型生成Mermaid
        reasoning_content = None
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                json={
                    "model": DEEPSEEK_REASONER_MODEL,
                    "messages": [
                        {"role": "user", "content": mermaid_prompt}
                    ],
                    "max_tokens": 4000
                },
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=90.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"API调用失败: {response.status_code}")
            
            data = response.json()
            message = data["choices"][0]["message"]
            
            # 提取思考过程
            if "reasoning_content" in message:
                reasoning_content = message["reasoning_content"]
                print(f"Reasoner思考过程: {reasoning_content[:200]}...")
            
            mermaid_content = message["content"].strip()
            
            # 清理Mermaid内容
            if "```mermaid" in mermaid_content:
                mermaid_content = mermaid_content.split("```mermaid")[1].split("```")[0].strip()
            elif "```" in mermaid_content:
                mermaid_content = mermaid_content.split("```")[1].split("```")[0].strip()
            
            # 验证mindmap格式
            if not mermaid_content.strip().startswith("mindmap"):
                raise HTTPException(status_code=500, detail="生成的Mermaid代码格式不正确：缺少mindmap关键字")
            
            print("Mermaid思维导图生成成功")
        
        # 4. 保存文件
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MindMap_{timestamp}"
        
        # 保存.mmd文件
        diagram_filename = f"{filename}.mmd"
        diagram_path = os.path.join(DIAGRAM_DIR, diagram_filename)
        with open(diagram_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        # 保存TXT文件（包含Mermaid代码）
        txt_filename = f"{filename}.txt"
        txt_path = os.path.join(DIAGRAM_DIR, txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        # 5. 生成简要说明
        summary = f"Mermaid mindmap - Generated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return {
            "status": "success",
            "type": "mermaid",
            "filename": filename,
            "diagram_filename": diagram_filename,
            "txt_filename": txt_filename,
            "diagram_url": f"/diagrams/{diagram_filename}",
            "txt_url": f"/diagrams/{txt_filename}",
            "summary": summary,
            "reasoning_content": reasoning_content,
            "message": "Mermaid思维导图生成成功"
        }
        
        # 保存TXT文件（包含代码）
        txt_filename = f"{filename}.txt"
        txt_path = os.path.join(DIAGRAM_DIR, txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(diagram_content)
        
        # 6. 生成简要说明
        type_label = "DrawIO" if diagram_type == "drawio" else "Mermaid"
        summary = f"{type_label} diagram - Generated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return {
            "status": "success",
            "type": diagram_type,
            "filename": filename,
            "diagram_filename": diagram_filename,
            "txt_filename": txt_filename,
            "diagram_url": f"/diagrams/{diagram_filename}",
            "txt_url": f"/diagrams/{txt_filename}",
            "summary": summary,
            "reasoning_content": reasoning_content,
            "message": f"{type_label}思维导图生成成功"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"生成思维导图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成思维导图失败: {str(e)}")

@app.get("/api/models")
async def list_models():
    """获取可用的模型列表"""
    return {
        "provider": "deepseek",
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "description": "DeepSeek的通用聊天模型"}
        ]
    }

@app.post("/api/generate-quiz")
async def generate_quiz(request: QuizRequest):
    """
    基于文档内容生成Quiz题目
    """
    try:
        if not request.documents:
            raise HTTPException(status_code=400, detail="需要至少一个文档来生成Quiz")
        
        # 构建文档内容
        doc_content = ""
        for idx, doc in enumerate(request.documents, 1):
            doc_content += f"--- 文档 {idx}: {doc.name} ---\n"
            doc_content += f"{doc.content[:5000]}\n\n"  # 限制每个文档最多5000字符
        
        # 使用DeepSeek模型生成Quiz
        prompt = f"""基于以下文档内容，生成5个四选一的选择题。

要求：
1. 题目应该测试对文档核心内容的理解
2. 难度适中，既不太简单也不太难
3. 每题有4个选项（A、B、C、D），只有1个正确答案
4. 干扰项要合理，不能明显错误
5. 必须严格按照以下JSON格式输出，不要添加任何其他文字说明：

{{
  "questions": [
    {{
      "question": "题目内容",
      "options": ["A选项", "B选项", "C选项", "D选项"],
      "correct_answer": 0,
      "explanation": "答案解释"
    }}
  ]
}}

注意：correct_answer是索引（0-3），0代表A，1代表B，2代表C，3代表D

文档内容：
{doc_content}"""
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的题目出题助手，擅长基于文档内容生成高质量的测试题目。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"DeepSeek API错误: {response.text}")
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 解析JSON响应
            try:
                # 提取JSON部分（可能包含代码块）
                json_match = re.search(r'```json\s*(.+?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = content
                
                quiz_data = json.loads(json_str)
                return quiz_data
            except json.JSONDecodeError as e:
                # 如果JSON解析失败，返回错误
                raise HTTPException(status_code=500, detail=f"AI响应格式错误: {str(e)}")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成Quiz失败: {str(e)}")

@app.post("/api/analyze-data")
async def analyze_data(request: DataAnalysisRequest):
    """
    分析文档中的数据并生成可视化
    """
    try:
        if not request.documents:
            raise HTTPException(status_code=400, detail="需要至少一个文档来进行数据分析")
        
        # 1. 提取文档中的数据
        doc_content = ""
        for idx, doc in enumerate(request.documents, 1):
            doc_content += f"--- 文档 {idx}: {doc.name} ---\n"
            doc_content += f"{doc.content[:8000]}\n\n"  # 限制每个文档最多8000字符
        
        # 2. 使用Reasoner模型分析数据
        analysis_prompt = f"""请分析以下文档内容，识别其中的数据并进行统计分析。

## 文档内容：
{doc_content}

## 任务要求：
1. **数据识别**：检查对话中是否包含数值数据、表格数据或统计数据
2. **数据提取**：如果存在数据，提取并整理成结构化格式
3. **统计分析**：进行描述性统计（均值、中位数、标准差、最大值、最小值等）
4. **可视化建议**：推荐合适的图表类型（柱状图、折线图、散点图、饼图等）
5. **Python代码生成**：生成完整的数据分析和可视化代码（使用matplotlib和pandas）

## 输出格式：
如果发现数据，请输出JSON格式：
```json
{{
  "has_data": true,
  "data_description": "数据描述",
  "statistics": {{"mean": 值, "median": 值, "std": 值, "min": 值, "max": 值}},
  "chart_type": "图表类型",
  "python_code": "完整的Python代码"
}}
```

如果没有发现数据，请输出：
```json
{{
  "has_data": false,
  "message": "对话中未发现可分析的数值数据"
}}
```

**要求：直接输出JSON，不要其他解释。**
"""
        
        reasoning_content = None
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                json={
                    "model": DEEPSEEK_REASONER_MODEL,
                    "messages": [
                        {"role": "user", "content": analysis_prompt}
                    ],
                    "max_tokens": 4000
                },
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=90.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"API调用失败: {response.status_code}")
            
            data = response.json()
            message = data["choices"][0]["message"]
            
            # 提取思考过程
            if "reasoning_content" in message:
                reasoning_content = message["reasoning_content"]
                print(f"Reasoner思考过程: {reasoning_content[:200]}...")
            
            analysis_result = message["content"].strip()
            
            # 清理JSON内容
            if "```json" in analysis_result:
                analysis_result = analysis_result.split("```json")[1].split("```")[0].strip()
            elif "```" in analysis_result:
                analysis_result = analysis_result.split("```")[1].split("```")[0].strip()
            
            # 解析JSON
            import json
            result_data = json.loads(analysis_result)
            
            # 检查是否有数据
            if not result_data.get("has_data", False):
                return {
                    "status": "no_data",
                    "message": result_data.get("message", "对话中未发现可分析的数据"),
                    "reasoning_content": reasoning_content
                }
            
            # 3. 执行Python代码生成可视化
            python_code = result_data.get("python_code", "")
            
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"DataAnalysis_{timestamp}"
            image_filename = f"{filename}.png"
            image_path = os.path.join(DIAGRAM_DIR, image_filename)
            
            # 保存代码文件
            code_filename = f"{filename}.py"
            code_path = os.path.join(DIAGRAM_DIR, code_filename)
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
            
            # 执行代码生成图表
            try:
                # 准备执行环境
                import matplotlib
                matplotlib.use('Agg')  # 使用非GUI后端
                import matplotlib.pyplot as plt
                import pandas as pd
                import numpy as np
                
                # 执行代码
                exec_globals = {
                    'plt': plt,
                    'pd': pd,
                    'np': np,
                    'output_path': image_path
                }
                
                # 修改代码以保存到指定路径 - 使用原始字符串避免转义问题
                # 将Windows路径的反斜杠转换为正斜杠或双反斜杠
                safe_image_path = image_path.replace('\\', '/')
                modified_code = python_code.replace(
                    "plt.show()",
                    f"plt.savefig('{safe_image_path}', dpi=300, bbox_inches='tight')\nplt.close()"
                )
                if "plt.savefig" not in modified_code and "plt.show()" not in modified_code:
                    modified_code += f"\nplt.savefig('{safe_image_path}', dpi=300, bbox_inches='tight')\nplt.close()"
                
                exec(modified_code, exec_globals)
                print(f"图表生成成功: {image_path}")
                
            except Exception as e:
                print(f"图表生成失败: {str(e)}")
                # 创建一个简单的错误图表
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.text(0.5, 0.5, f"图表生成失败\n{str(e)}", 
                       ha='center', va='center', fontsize=12, color='red')
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
                plt.savefig(image_path, dpi=300, bbox_inches='tight')
                plt.close()
            
            # 4. 生成统计报告文本
            stats_text = f"""# 数据分析报告

## 数据描述
{result_data.get('data_description', 'N/A')}

## 描述性统计
{json.dumps(result_data.get('statistics', {}), indent=2, ensure_ascii=False)}

## 可视化类型
{result_data.get('chart_type', 'N/A')}

## Python代码
```python
{python_code}
```
"""
            
            txt_filename = f"{filename}.txt"
            txt_path = os.path.join(DIAGRAM_DIR, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(stats_text)
            
            summary = f"Data analysis - Generated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            return {
                "status": "success",
                "filename": filename,
                "image_filename": image_filename,
                "code_filename": code_filename,
                "txt_filename": txt_filename,
                "image_url": f"/diagrams/{image_filename}",
                "code_url": f"/diagrams/{code_filename}",
                "txt_url": f"/diagrams/{txt_filename}",
                "summary": summary,
                "data_description": result_data.get('data_description', ''),
                "statistics": result_data.get('statistics', {}),
                "chart_type": result_data.get('chart_type', ''),
                "reasoning_content": reasoning_content,
                "message": "数据分析完成"
            }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"数据分析失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"数据分析失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("NotebookLLM Backend with DeepSeek API")
    print("API Key configured: " + ("✓" if DEEPSEEK_API_KEY else "✗"))
    print("Demo Mode: " + ("ON" if DEMO_MODE else "OFF"))
    print("Running on http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
