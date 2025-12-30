# 🚀 立即开始使用 NotebookLLM - DeepSeek版本

## ⚡ 5分钟快速启动

### 步骤1️⃣: 获取DeepSeek API密钥 (2分钟)

```
1. 打开: https://platform.deepseek.com/api_keys
2. 登录或注册DeepSeek账户
3. 点击"创建新密钥"
4. 复制密钥 (格式: sk-xxx...)
```

### 步骤2️⃣: 配置API密钥 (1分钟)

**Windows用户:**
```powershell
# 打开 backend/main.py
# 找到第17行:
# DEEPSEEK_API_KEY = "sk-f4d9eb02ce5143f1b3c3a4b3eb42c37b"
# 替换为您的密钥:
DEEPSEEK_API_KEY = "sk-your-key-here"
```

### 步骤3️⃣: 启动后端 (1分钟)

**方式A: PowerShell (Windows推荐) ⭐**
```powershell
# 打开PowerShell，进入项目目录
cd c:\Users\35696\mynotebookllm
.\run_backend.ps1
```

**方式B: 命令行**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**方式C: Docker**
```bash
docker build -t notebookllm .
docker run -p 8000:8000 notebookllm
```

### 步骤4️⃣: 打开应用 (1分钟)

在浏览器打开:
```
http://localhost:8000
```

---

## ✅ 验证应用是否正常

### 检查清单
- [ ] 后端显示 "Running on http://0.0.0.0:8000"
- [ ] 浏览器打开 http://localhost:8000
- [ ] 看到NotebookLLM界面
- [ ] 可以输入消息
- [ ] AI正常回复

### 运行测试脚本

```powershell
# 在另一个PowerShell窗口
python test_deepseek.py
```

预期输出:
```
✅ DeepSeek API连接成功!
✅ 后端服务运行正常!
✅ 后端聊天接口正常!
✅ 对话历史功能正常!

🎉 所有测试通过! 应用已准备好使用。
```

---

## 🎯 主要功能说明

### 左侧 Sources 面板
- 📄 导入研究文献
- 🔍 搜索和过滤
- 🎓 Deep Research工具

### 中间 Chat 面板
- 💬 与AI聊天
- 📚 完整的对话历史
- ⚡ 实时回复

### 右侧 Studio 面板
- 🎵 **Audio Overview** - 音频概述
- 🎬 **Video Overview** - 视频概述
- 🧠 **Mind Map** - 思维导图
- 📊 **Reports** - 研究报告
- 📇 **Flashcards** - 抽认卡
- 📈 **Infographic** - 信息图表
- 📋 **Data Table** - 数据表格
- 🧪 **Quiz** - 测验

---

## 🔧 常见问题

### Q: 后端无法启动?
**A:** 检查Python版本和依赖
```bash
python --version  # 需要3.8+
pip install fastapi uvicorn httpx
```

### Q: 前端无法连接后端?
**A:** 确保后端运行在正确的地址
```bash
# 检查后端是否运行
curl http://localhost:8000/health
```

### Q: 出现"Unauthorized"错误?
**A:** API密钥不正确
1. 检查 `backend/main.py` 第17行
2. 确认密钥有效 (https://platform.deepseek.com/api_keys)
3. 确认有足够的额度

### Q: 回复很慢?
**A:** 尝试调整参数
```python
# 在 backend/main.py 中修改:
"temperature": 0.5,  # 降低创意度可加快速度
"max_tokens": 1024   # 减少生成长度
```

---

## 📚 完整文档

- **README.md** - 项目概览
- **CONFIG.md** - 配置详情
- **API.md** - API文档
- **DEPLOYMENT.md** - 部署指南

---

## 🎓 使用示例

### 例子1: 学术讨论
```
用户: "请分析《人工智能基础》这本书的核心内容"
AI: [详细分析...]

用户: "这些内容与现在的深度学习有什么关联?"
AI: [深度分析...]
```

### 例子2: 代码讨论
```
用户: "解释一下这个Python异步代码"
AI: [代码解析...]

用户: "如何优化性能?"
AI: [优化建议...]
```

### 例子3: 创意写作
```
用户: "帮我构思一个科幻故事框架"
AI: [故事大纲...]

用户: "主角应该有什么背景?"
AI: [角色设定...]
```

---

## 🚀 下一步

### 进阶配置
1. 修改温度和生成长度参数
2. 集成自定义文档库
3. 添加用户认证系统
4. 部署到云平台

### 功能扩展
1. 实现Sources面板上传功能
2. 完成Studio各工具的后端逻辑
3. 添加数据持久化
4. 实现对话导出功能

### 部署上线
1. 购买域名
2. 获取SSL证书
3. 部署到云服务 (AWS/Google Cloud/Heroku)
4. 配置CDN加速

---

## 💡 性能优化提示

### 前端优化
- 使用浏览器缓存
- 压缩静态文件
- 懒加载消息历史

### 后端优化
- 使用数据库存储对话
- 实现请求队列
- 添加响应缓存

### LLM优化
- 调整temperature为0.5
- 减少max_tokens
- 使用更快的模型版本

---

## 🆘 获取帮助

### 官方资源
- **DeepSeek文档**: https://docs.deepseek.com/
- **FastAPI文档**: https://fastapi.tiangolo.com/
- **httpx文档**: https://www.python-httpx.org/

### 调试技巧
```bash
# 启用详细日志
python -u backend/main.py

# 测试API连接
python test_deepseek.py

# 检查网络连接
ping api.deepseek.com
```

---

**祝您使用愉快! 🎉**

如有任何问题，欢迎反馈！
