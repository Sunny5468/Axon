# 🎙️ NotebookLLM - AI讨论生成器

将您的笔记和文档转化为**AI生成的自然对话讨论**。模仿 Google NotebookLLM 的功能，使用OpenAI API生成两个虚拟讲者之间的深度讨论。

<div align="center">

![NotebookLLM](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

[快速开始](#-快速开始) • [使用教程](#-使用指南) • [API文档](#-api端点) • [部署指南](DEPLOYMENT.md)

</div>

---

## ✨ 核心特性

### 🎯 主要功能
- **📄 多种输入方式** - 上传文件或直接输入文本
- **🤖 AI生成讨论** - 使用OpenAI API生成自然对话
- **⚙️ 灵活配置** - 调整讨论深度、长度、语气
- **🎨 优美界面** - 现代化的紫色渐变设计
- **⚡ 快速响应** - 支持gpt-3.5-turbo和gpt-4

### 🔧 技术特点
- **前端** - 纯HTML/CSS/JavaScript，无需框架
- **后端** - FastAPI异步框架，支持多LLM服务商
- **API** - RESTful接口，完整的Swagger文档
- **跨平台** - Windows/macOS/Linux一键启动

---

## 📋 项目结构

```
mynotebookllm/
├── frontend/                   # 前端应用
│   ├── index.html             # 单文件应用（HTML+CSS+JS）
│   └── package.json           # 项目配置
├── backend/                    # Python后端
│   ├── main.py               # 基础版本
│   ├── main_enhanced.py      # 增强版本（多LLM支持）
│   ├── requirements.txt       # Python依赖
│   └── .env.example          # 环境变量模板
├── 📚 文档
│   ├── README.md             # 项目说明
│   ├── QUICKSTART.md         # 快速开始
│   ├── USAGE.md              # 详细使用教程
│   ├── DEPLOYMENT.md         # 部署指南
│   ├── CONFIG.md             # 配置参考
│   └── PROJECT_STRUCTURE.md  # 项目架构
├── 🚀 启动脚本
│   ├── run_backend.bat       # Windows后端启动
│   ├── run_frontend.bat      # Windows前端启动
│   ├── run_backend.sh        # macOS/Linux后端
│   └── run_frontend.sh       # macOS/Linux前端
└── .github/                   # GitHub配置
    └── copilot-instructions.md
```

## 🚀 快速开始

### 前置条件

- **Python 3.8+**
- **互联网连接** - 调用OpenAI API
- **API密钥** - 已内置 `sk-5610a05204284964a0953677a117a9dd`

### Windows用户（最简单）

```bash
# 1. 启动后端 (双击或运行)
run_backend.bat

# 2. 启动前端 (新建命令行，双击或运行)
run_frontend.bat

# 3. 打开浏览器
访问 http://localhost:3000
```

### macOS/Linux用户

```bash
# 1. 启动后端
chmod +x run_backend.sh
./run_backend.sh &

# 2. 启动前端 (新终端)
chmod +x run_frontend.sh
./run_frontend.sh

# 3. 打开浏览器
访问 http://localhost:3000
```

### 手动启动

**后端：**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**前端：** (新建命令行)
```bash
cd frontend
python -m http.server 3000
```

然后在浏览器打开：`http://localhost:3000`

### ✅ 验证安装

打开浏览器访问：
- 前端: `http://localhost:3000` ✓
- API: `http://localhost:8000/health` ✓
- 文档: `http://localhost:8000/docs` ✓

## 💡 功能特点

### 前端功能
- 📄 **文件上传** - 支持TXT、PDF、DOCX格式
- ✏️ **文本输入** - 直接粘贴笔记内容
- ⚙️ **讨论设置**
  - 话题深度：浅层、中等、深层
  - 对话长度：短篇、中等、长篇
  - 语气风格：专业、随意、教育、娱乐
  - 自定义讲者名称
- 🎬 **实时显示** - 动态展示生成的讨论内容
- 📱 **响应式设计** - 支持桌面和移动设备

### 后端功能
- 🤖 **AI生成** - 使用OpenAI API生成自然讨论
- 📝 **智能解析** - 自动解析和格式化讨论内容
- 🔄 **异步处理** - 高效处理并发请求
- 📊 **REST API** - 完整的RESTful接口
- 🔌 **多LLM支持** - OpenAI和Anthropic Claude（增强版）
- 📚 **自动文档** - Swagger/OpenAPI交互文档

---

## 📖 使用指南

### 基本步骤

1. **上传或输入内容**
   - 选择"上传文件"或"直接输入文本"
   - 粘贴或选择您的笔记

2. **配置参数**
   - 调整讨论深度、长度、语气
   - 输入讲者名称（可选）

3. **生成讨论**
   - 点击"🚀 生成讨论"按钮
   - 等待AI生成对话

4. **查看结果**
   - 讨论内容显示在底部面板
   - 可复制或保存讨论

### 推荐设置

| 场景 | 深度 | 长度 | 语气 | 讲者 |
|------|------|------|------|------|
| 学习复习 | 深层 | 中等 | 教育 | 老师/学生 |
| 快速了解 | 浅层 | 短篇 | 随意 | 讲者1/讲者2 |
| 商务讨论 | 中等 | 中等 | 专业 | 主管/员工 |
| 娱乐讨论 | 中等 | 短篇 | 幽默 | 任意 |

详细教程见：[USAGE.md](USAGE.md)

## 🔌 API端点

### 核心端点

#### 生成讨论 ⭐
```
POST /api/generate
Content-Type: application/json
```

**请求参数：**
```json
{
  "content": "您的笔记或文档内容",
  "depth": "medium",              // shallow | medium | deep
  "length": "medium",             // short | medium | long
  "tone": "professional",         // professional | casual | educational | entertaining
  "speaker1": "讲者1",
  "speaker2": "讲者2",
  "provider": "openai",           // openai | anthropic (可选)
  "model": "gpt-3.5-turbo"        // 模型名称 (可选)
}
```

**响应示例：**
```json
{
  "status": "success",
  "discussion": [
    {
      "speaker": "讲者1",
      "text": "您好，今天我们来讨论一下..."
    },
    {
      "speaker": "讲者2",
      "text": "好的，我认为首先要理解..."
    }
  ],
  "meta": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "items_count": 2
  }
}
```

### 其他端点

#### 健康检查
```
GET /health
```
检查后端服务是否运行正常

#### 获取模型列表
```
GET /api/models?provider=openai
```
返回可用的LLM模型列表

#### 获取供应商列表
```
GET /api/providers
```
返回支持的LLM供应商列表

#### API主页
```
GET /
```
获取API信息和版本

#### 交互式文档
```
访问 http://localhost:8000/docs
```
Swagger UI文档，可直接测试API

---

## 🔑 配置说明

### API密钥配置

**方法1：环境变量（推荐）**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-5610a05204284964a0953677a117a9dd"

# Windows CMD
set OPENAI_API_KEY=sk-5610a05204284964a0953677a117a9dd

# macOS/Linux
export OPENAI_API_KEY="sk-5610a05204284964a0953677a117a9dd"
```

**方法2：.env文件**
```bash
# 在 backend 目录创建 .env 文件
OPENAI_API_KEY=sk-5610a05204284964a0953677a117a9dd
ANTHROPIC_API_KEY=  # 如果使用Claude
```

**方法3：直接修改代码**
```python
# backend/main.py
API_KEYS = {
    "openai": "sk-5610a05204284964a0953677a117a9dd",
}
```

### 模型选择

**GPT-3.5-turbo** (推荐)
- ✅ 速度快（30-60秒）
- ✅ 成本低
- ✅ 质量良好
- 用于：快速讨论、日常使用

**GPT-4**
- ✅ 质量最好
- ❌ 速度较慢（60-120秒）
- ❌ 成本较高
- 用于：高质量讨论、学术场景

**GPT-4 Turbo**
- ✅ 速度中等
- ✅ 质量很好
- ✅ 成本适中
- 用于：平衡质量和速度

---

## 🎯 使用场景

## 🎯 使用场景

### 📚 学习和教育
- 将课程笔记转化为师生讨论
- 快速复习重点知识
- 理解不同观点的碰撞

### 📰 新闻和评论
- 将文章转化为评论讨论
- 分析社论的不同角度
- 理解复杂话题的多面性

### 💼 商务和工作
- 产品说明书转化为销售讨论
- 会议记录转化为要点讨论
- 策略文件转化为团队讨论

### 📖 创意写作
- 故事大纲转化为人物对话
- 小说章节转化为评论讨论
- 剧本创作前的思路碰撞

---

## 🔧 高级配置

### 修改LLM服务商

要使用不同的LLM（如Claude）：

1. 在 `backend/main_enhanced.py` 中已支持
2. 修改API密钥配置
3. 在请求中指定provider参数

```python
# 使用Claude替代GPT
{
  "content": "文档内容",
  "provider": "anthropic",
  "model": "claude-3-sonnet-20240229"
}
```

### 调整生成参数

编辑 `backend/main.py` 中的 `call_openai_api` 函数：

```python
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [...],
    "temperature": 0.7,      # 调整：0.0-1.0（越低越确定）
    "max_tokens": 4000,      # 最大输出长度
    "top_p": 0.9,           # 核采样参数
}
```

### 自定义UI样式

编辑 `frontend/index.html` 中的 `<style>` 部分：

```css
/* 修改主题颜色 */
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);

/* 修改按钮样式 */
.btn { background: #YOUR_COLOR; }

/* 修改字体 */
body { font-family: 'Your Font', sans-serif; }
```

---

## 🐛 故障排除

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| 后端无法启动 | 端口占用或Python版本低 | 更换端口或升级Python |
| 前端无法连接 | 后端未运行或CORS问题 | 确保后端运行，检查CORS配置 |
| API密钥无效 | 密钥错误或已过期 | 检查和更新API密钥 |
| 生成超时 | 网络慢或API响应慢 | 减少讨论长度或更换模型 |
| 讨论格式错误 | LLM返回格式异常 | 更换模型或重新生成 |

### 调试技巧

1. **查看前端错误**
   - 按 F12 打开开发者工具
   - 查看 Console 标签的错误信息
   - 查看 Network 标签的API响应

2. **查看后端日志**
   - 运行后端的终端窗口显示详细日志
   - 查找 ERROR 或 WARNING 信息

3. **测试API**
   ```bash
   curl -X GET "http://localhost:8000/health"
   ```

4. **查看完整文档**
   - 访问 `http://localhost:8000/docs`
   - 使用Swagger UI测试API

详细故障排除见：[DEPLOYMENT.md](DEPLOYMENT.md#-常见问题)

## 📦 依赖说明

### 前端
- **HTML5** - 页面结构
- **CSS3** - 样式和动画（无框架）
- **Vanilla JavaScript** - 交互逻辑（无依赖）
- ✨ **零依赖** - 只需浏览器即可运行

### 后端

| 依赖 | 版本 | 用途 |
|------|------|------|
| **fastapi** | 0.104.1 | Web框架 |
| **uvicorn** | 0.24.0 | ASGI服务器 |
| **httpx** | 0.25.0 | 异步HTTP客户端 |
| **pydantic** | 2.5.0 | 数据验证 |
| **python-multipart** | 0.0.6 | 表单数据处理 |

---

## 🔐 安全建议

### 开发环境 ✅
- API密钥可以在代码中或环境变量中
- 无需HTTPS
- CORS允许所有源

### 生产环境 ⚠️

1. **使用环境变量**
   ```bash
   export OPENAI_API_KEY="sk-xxxx"
   ```

2. **启用HTTPS**
   - 使用Let's Encrypt或其他证书
   - 配置Nginx反向代理

3. **限制API访问**
   - 添加速率限制
   - 实现用户认证
   - 添加请求验证

4. **定期更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

详见：[DEPLOYMENT.md](DEPLOYMENT.md#-生产环境建议)

---

## 📈 扩展功能路线图

### 短期 (易实现)
- [ ] 讨论历史记录保存
- [ ] 导出为PDF/Markdown
- [ ] 亮色/暗色主题切换
- [ ] 多语言支持

### 中期 (需要修改)
- [ ] 文本转语音（TTS）生成音频
- [ ] 用户账户和登录
- [ ] 数据库存储讨论
- [ ] 讨论内容评分反馈
- [ ] 更多LLM支持（Google、Cohere等）

### 长期 (重大升级)
- [ ] React/Vue前端重构
- [ ] 移动APP（iOS/Android）
- [ ] 实时流式传输
- [ ] 团队协作功能
- [ ] 讨论内容深度分析
- [ ] 自定义AI讲者个性

---

## 📚 文档导航

| 文档 | 内容 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | 30秒快速开始 |
| [USAGE.md](USAGE.md) | 详细使用教程和技巧 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 部署和配置指南 |
| [CONFIG.md](CONFIG.md) | 配置参考和说明 |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 项目架构详解 |

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建您的分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 许可证

本项目采用 **MIT License** - 详见 [LICENSE](LICENSE) 文件

---

## 📞 获取帮助

### 常见问题
- 查看 [USAGE.md](USAGE.md#常见错误与解决) 的故障排除部分
- 访问 `http://localhost:8000/docs` 查看完整API文档

### 提交问题
- 在GitHub上提交Issue
- 附带错误日志和重现步骤
- 说明您的操作系统和Python版本

### 扩展支持
- 修改 `backend/main_enhanced.py` 添加新的LLM服务商
- 修改 `frontend/index.html` 自定义UI样式

---

## 🙏 致谢

- 灵感来自 [Google NotebookLLM](https://notebooklm.google/)
- 由 [OpenAI](https://openai.com/) API提供支持
- 使用 [FastAPI](https://fastapi.tiangolo.com/) 构建

---

<div align="center">

**Made with ❤️ by NotebookLLM Contributors**

如果觉得有用，请给个Star ⭐

[⬆ 回到顶部](#-notebookllm---ai讨论生成器)

</div>
