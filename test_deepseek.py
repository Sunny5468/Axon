#!/usr/bin/env python3
"""
NotebookLLM - DeepSeek API测试脚本
用于验证后端与DeepSeek API的连接
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

# 配置
DEEPSEEK_API_KEY = "sk-f4d9eb02ce5143f1b3c3a4b3eb42c37b"  # 替换为您的API密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
BACKEND_URL = "http://localhost:8000"

def print_header(text):
    """打印格式化的标题"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_status(status, message):
    """打印状态信息"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {message}")

async def test_deepseek_api():
    """测试DeepSeek API连接"""
    print_header("测试1: DeepSeek API直接连接")
    
    try:
        async with httpx.AsyncClient() as client:
            print(f"发送请求到: {DEEPSEEK_API_URL}")
            print(f"模型: {DEEPSEEK_MODEL}")
            print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            response = await client.post(
                DEEPSEEK_API_URL,
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Hello! This is a test message. Please respond briefly."
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            
            print(f"\n响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    reply = data["choices"][0]["message"]["content"]
                    print(f"AI回复: {reply}\n")
                    print_status(True, "DeepSeek API连接成功!")
                    return True
                else:
                    print_status(False, "响应格式错误")
                    print(f"响应内容: {data}\n")
                    return False
            else:
                error_text = response.text
                print_status(False, f"API错误: {response.status_code}")
                print(f"错误信息: {error_text}\n")
                return False
                
    except Exception as e:
        print_status(False, f"连接失败: {str(e)}\n")
        return False

async def test_backend_health():
    """测试后端健康状态"""
    print_header("测试2: 后端健康检查")
    
    try:
        async with httpx.AsyncClient() as client:
            print(f"检查后端: {BACKEND_URL}/health")
            
            response = await client.get(
                f"{BACKEND_URL}/health",
                timeout=5.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"响应: {json.dumps(data, indent=2)}\n")
                print_status(True, "后端服务运行正常!")
                return True
            else:
                print_status(False, f"后端返回错误: {response.status_code}\n")
                return False
                
    except Exception as e:
        print_status(False, f"无法连接后端: {str(e)}")
        print("💡 提示: 确保后端正在运行 (python backend/main.py)\n")
        return False

async def test_backend_chat():
    """测试后端聊天接口"""
    print_header("测试3: 后端聊天接口")
    
    try:
        async with httpx.AsyncClient() as client:
            print(f"发送聊天请求到: {BACKEND_URL}/api/chat")
            print(f"测试消息: 'Hello, how are you?'")
            
            response = await client.post(
                f"{BACKEND_URL}/api/chat",
                json={
                    "message": "Hello, how are you? This is a test from the frontend.",
                    "history": []
                },
                timeout=60.0
            )
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n后端响应:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                if "response" in data:
                    print_status(True, "后端聊天接口正常!")
                    return True
                else:
                    print_status(False, "响应格式错误")
                    return False
            else:
                error_text = response.text
                print(f"错误: {error_text}")
                print_status(False, f"后端返回错误: {response.status_code}\n")
                return False
                
    except Exception as e:
        print_status(False, f"连接失败: {str(e)}")
        print("💡 提示: 确保后端正在运行且配置正确\n")
        return False

async def test_conversation_history():
    """测试对话历史功能"""
    print_header("测试4: 对话历史功能")
    
    try:
        async with httpx.AsyncClient() as client:
            # 第一条消息
            print("发送第一条消息...")
            response1 = await client.post(
                f"{BACKEND_URL}/api/chat",
                json={
                    "message": "My name is Alice.",
                    "history": []
                },
                timeout=60.0
            )
            
            if response1.status_code != 200:
                print_status(False, "第一条消息失败\n")
                return False
            
            data1 = response1.json()
            first_reply = data1["response"]
            print(f"AI: {first_reply}\n")
            
            # 第二条消息（带历史）
            print("发送第二条消息（带历史）...")
            response2 = await client.post(
                f"{BACKEND_URL}/api/chat",
                json={
                    "message": "What is my name?",
                    "history": [
                        {"role": "user", "content": "My name is Alice."},
                        {"role": "assistant", "content": first_reply}
                    ]
                },
                timeout=60.0
            )
            
            if response2.status_code == 200:
                data2 = response2.json()
                second_reply = data2["response"]
                print(f"AI: {second_reply}\n")
                print_status(True, "对话历史功能正常!")
                return True
            else:
                print_status(False, "第二条消息失败\n")
                return False
                
    except Exception as e:
        print_status(False, f"测试失败: {str(e)}\n")
        return False

async def main():
    """主测试函数"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║  🚀 NotebookLLM - DeepSeek API 测试套件" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {}
    
    # 测试1: DeepSeek API
    results["DeepSeek API"] = await test_deepseek_api()
    await asyncio.sleep(1)
    
    # 测试2: 后端健康检查
    results["后端健康检查"] = await test_backend_health()
    await asyncio.sleep(1)
    
    # 测试3: 后端聊天接口
    results["后端聊天接口"] = await test_backend_chat()
    await asyncio.sleep(1)
    
    # 测试4: 对话历史
    results["对话历史功能"] = await test_conversation_history()
    
    # 生成总结
    print_header("📊 测试总结")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        emoji = "✅" if result else "❌"
        print(f"{emoji} {test_name}")
    
    print(f"\n总体: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过! 应用已准备好使用。")
        print("访问: http://localhost:8000")
        return 0
    else:
        print("\n⚠️ 部分测试失败。请检查配置和错误信息。")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
