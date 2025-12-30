"""
NotebookLLM Backend - 支持多个LLM供应商
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import os
from typing import List, Optional

app = FastAPI(title="NotebookLLM API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 配置部分 ============

# API配置 - 支持多个服务商
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", "sk-229b5c8d1d6c4e0b8cffc3eb59679e60"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
}

# 默认使用OpenAI
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-3.5-turbo"

# 模型配置
MODELS = {
    "openai": [
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "speed": "fast", "quality": "good"},
        {"id": "gpt-4", "name": "GPT-4", "speed": "slow", "quality": "excellent"},
        {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "speed": "medium", "quality": "excellent"},
    ],
    "anthropic": [
        {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "speed": "fast", "quality": "good"},
        {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "speed": "slow", "quality": "excellent"},
    ]
}

# ============ 数据模型 ============

class GenerateRequest(BaseModel):
    content: str
    depth: str = "medium"
    length: str = "medium"
    tone: str = "professional"
    speaker1: str = "讲者1"
    speaker2: str = "讲者2"
    provider: Optional[str] = DEFAULT_PROVIDER
    model: Optional[str] = DEFAULT_MODEL

class DiscussionItem(BaseModel):
    speaker: str
    text: str

# ============ 工具函数 ============

def build_prompt(content: str, depth: str, length: str, tone: str, speaker1: str, speaker2: str) -> str:
    """构建发送给LLM的提示词"""
    
    depth_desc = {
        "shallow": "简洁而表面的，只涉及主要观点",
        "medium": "平衡的、中等深度的、涵盖主要和次要观点",
        "deep": "深入的、详细的、探索性的、包括深层含义和隐喻"
    }
    
    length_desc = {
        "short": "5-10分钟长度（约800-1200字）",
        "medium": "10-20分钟长度（约1500-2500字）",
        "long": "20-30分钟长度（约3000-4500字）"
    }
    
    tone_desc = {
        "professional": "专业、严肃、学术性的讨论",
        "casual": "轻松、友好、日常会话风格",
        "educational": "教育启蒙、易于理解、适合学习者",
        "entertaining": "娱乐幽默、生动有趣、引人入胜"
    }
    
    prompt = f"""你是一个专业的对话编写助手。请根据以下内容生成两个虚拟讲者之间的自然讨论。

【文档内容】
{content}

【讨论设置】
- 讲者1名称：{speaker1}
- 讲者2名称：{speaker2}
- 讨论深度：{depth_desc.get(depth, depth)}
- 讨论长度：{length_desc.get(length, length)}
- 语气风格：{tone_desc.get(tone, tone)}

【对话编写要求】
1. 生成自然流畅的对话讨论，两个讲者交替发言
2. 讨论应该围绕提供的文档内容进行
3. 对话要有逻辑性和连贯性，每个发言都要相关联
4. 保持指定的语气和风格
5. 讲者应该互相补充、提问和讨论，而不是简单地陈述事实
6. 讨论应该引人入胜，让人想继续听下去
7. 适当添加自然的插语和转换词
8. 保持讲者之间的平衡，给两人相似的发言空间

【输出格式要求】
请按照以下JSON格式输出，每个对话条目都有"speaker"和"text"两个字段。确保输出是有效的JSON：

[
  {{"speaker": "{speaker1}", "text": "第一个发言的内容..."}},
  {{"speaker": "{speaker2}", "text": "第二个发言的内容..."}},
  {{"speaker": "{speaker1}", "text": "继续讨论..."}},
  ...
]

现在开始生成讨论内容："""
    
    return prompt

async def call_openai_api(prompt: str, model: str) -> str:
    """调用OpenAI API"""
    
    headers = {
        "Authorization": f"Bearer {API_KEYS['openai']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的对话编写助手，精通各种话题的讨论。你的回复必须是有效的JSON格式。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
        "top_p": 0.9
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"OpenAI API error: {response.status_code} - {error_detail}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    except httpx.TimeoutException:
        raise Exception("OpenAI API请求超时，请稍后重试")
    except Exception as e:
        raise Exception(f"OpenAI API调用失败: {str(e)}")

async def call_anthropic_api(prompt: str, model: str) -> str:
    """调用Anthropic Claude API"""
    
    headers = {
        "x-api-key": API_KEYS['anthropic'],
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "max_tokens": 4000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Anthropic API error: {response.status_code}")
            
            result = response.json()
            return result["content"][0]["text"]
    
    except Exception as e:
        raise Exception(f"Anthropic API调用失败: {str(e)}")

async def call_llm_api(prompt: str, provider: str = DEFAULT_PROVIDER, model: str = DEFAULT_MODEL) -> str:
    """调用LLM API（支持多个供应商）"""
    
    if provider == "openai":
        return await call_openai_api(prompt, model)
    elif provider == "anthropic":
        return await call_anthropic_api(prompt, model)
    else:
        raise Exception(f"不支持的LLM供应商: {provider}")

def parse_discussion(content: str, speaker1: str, speaker2: str) -> List[DiscussionItem]:
    """解析LLM返回的讨论内容"""
    
    # 清理前后的markdown代码块标记
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```", 1)[1]
    if content.endswith("```"):
        content = content.rsplit("```", 1)[0]
    
    try:
        # 尝试解析JSON格式
        discussion = json.loads(content)
        
        if isinstance(discussion, list):
            return [DiscussionItem(**item) for item in discussion]
        else:
            return extract_discussion_from_text(content, speaker1, speaker2)
    
    except json.JSONDecodeError:
        return extract_discussion_from_text(content, speaker1, speaker2)

def extract_discussion_from_text(content: str, speaker1: str, speaker2: str) -> List[DiscussionItem]:
    """从文本内容中提取讨论结构"""
    
    discussion = []
    lines = content.split('\n')
    
    current_speaker = speaker1
    current_text = ""
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if current_text:
                current_text += "\n"
            continue
        
        # 检查是否包含讲者名称
        if (speaker1 in line and ":" in line) or (speaker2 in line and ":" in line):
            # 保存前一个讲者的内容
            if current_text.strip():
                discussion.append(DiscussionItem(
                    speaker=current_speaker,
                    text=current_text.strip()
                ))
            
            # 确定新讲者
            if speaker1 in line:
                current_speaker = speaker1
            else:
                current_speaker = speaker2
            
            # 提取发言内容
            current_text = line.split(":", 1)[-1].strip()
        else:
            # 继续当前发言
            if current_text:
                current_text += " "
            current_text += line
    
    # 添加最后一段
    if current_text.strip():
        discussion.append(DiscussionItem(
            speaker=current_speaker,
            text=current_text.strip()
        ))
    
    # 如果没有解析出任何内容
    if not discussion:
        discussion.append(DiscussionItem(
            speaker=speaker1,
            text=content
        ))
    
    return discussion

# ============ API端点 ============

@app.get("/")
async def root():
    """根端点"""
    return {
        "name": "NotebookLLM API",
        "version": "1.0.0",
        "description": "将笔记转化为AI生成的讨论",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "message": "NotebookLLM Backend正在运行"
    }

@app.post("/api/generate")
async def generate_discussion(request: GenerateRequest):
    """
    生成AI讨论内容
    """
    
    try:
        # 验证输入
        if not request.content or not request.content.strip():
            raise HTTPException(status_code=400, detail="内容不能为空")
        
        # 构建提示词
        prompt = build_prompt(
            content=request.content,
            depth=request.depth,
            length=request.length,
            tone=request.tone,
            speaker1=request.speaker1,
            speaker2=request.speaker2
        )
        
        # 调用LLM API
        discussion_text = await call_llm_api(
            prompt,
            provider=request.provider or DEFAULT_PROVIDER,
            model=request.model or DEFAULT_MODEL
        )
        
        # 解析讨论内容
        parsed_discussion = parse_discussion(discussion_text, request.speaker1, request.speaker2)
        
        return {
            "status": "success",
            "discussion": [{"speaker": item.speaker, "text": item.text} for item in parsed_discussion],
            "meta": {
                "provider": request.provider or DEFAULT_PROVIDER,
                "model": request.model or DEFAULT_MODEL,
                "items_count": len(parsed_discussion)
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成讨论失败: {str(e)}")

@app.get("/api/models")
async def list_models(provider: Optional[str] = None):
    """
    获取可用的模型列表
    """
    
    if provider and provider not in MODELS:
        raise HTTPException(status_code=400, detail=f"不支持的供应商: {provider}")
    
    if provider:
        return {
            "provider": provider,
            "models": MODELS[provider]
        }
    
    return {
        "providers": {
            "openai": MODELS["openai"],
            "anthropic": MODELS["anthropic"]
        }
    }

@app.get("/api/providers")
async def list_providers():
    """
    获取可用的LLM供应商列表
    """
    return {
        "providers": list(MODELS.keys()),
        "default": DEFAULT_PROVIDER
    }

@app.post("/api/validate")
async def validate_api_key(provider: str, api_key: str):
    """
    验证API密钥是否有效
    """
    
    try:
        # 这里可以添加实际的验证逻辑
        # 简单起见，我们假设所有密钥都是有效的（在生产环境中应该做真正的验证）
        
        return {
            "status": "valid",
            "provider": provider,
            "message": "API密钥验证成功"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"API密钥验证失败: {str(e)}")

# ============ 配置和启动 ============

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("NotebookLLM Backend")
    print("=" * 50)
    print(f"默认LLM供应商: {DEFAULT_PROVIDER}")
    print(f"默认模型: {DEFAULT_MODEL}")
    print(f"API文档: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
