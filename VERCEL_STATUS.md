# Vercel 部署功能状态

## ✅ 已实现的功能

### 1. 聊天对话 (`/api/chat`)
- ✅ DeepSeek API 集成
- ✅ 流式输出（逐字显示）
- ✅ 对话历史记录
- ✅ 文档上下文支持
- ✅ 自动使用环境变量中的 API 密钥

### 2. 文件上传 (`/api/upload`)
- ✅ PDF 文件解析 (PyPDF2)
- ✅ TXT 文件解析（支持 UTF-8 和 GBK 编码）
- ✅ 文件大小限制：4.5MB（Vercel 限制 5MB）
- ❌ 不支持 DOCX（python-docx 在 Vercel 上有兼容性问题）

### 3. 网页爬取 (`/api/crawl`)
- ✅ 抓取任意 URL 的网页内容
- ✅ 自动去除 HTML 标签
- ✅ 提取纯文本内容
- ✅ 超时限制：10 秒

### 4. 健康检查 (`/api/health`)
- ✅ API 状态检查
- ✅ API 密钥配置检查

## ❌ 未实现的功能（Vercel 限制）

### 1. 音频处理 (`/api/audio-to-text`)
**原因：** Vercel Serverless Functions 不支持：
- 无文件系统持久化（无法保存音频文件）
- 无 FFmpeg 等音频处理工具
- 执行时间限制（10-60秒）

**返回：** 501 Not Implemented

### 2. 思维导图生成 (`/api/generate-mindmap`)
**原因：** 需要：
- 文件系统存储（保存 .mmd/.drawio 文件）
- 可能需要 Graphviz 等绘图工具

**返回：** 501 Not Implemented

### 3. 数据分析 (`/api/data-analysis`)
**原因：** 需要：
- Python 数据分析库（pandas, matplotlib）
- 文件系统存储（保存生成的代码和图表）
- 可能需要更长的执行时间

**返回：** 501 Not Implemented

### 4. 测验生成 (`/api/generate-quiz`)
**原因：** 需要：
- 文件系统存储（保存测验文件）
- 可能需要额外的格式化处理

**返回：** 501 Not Implemented

## 🔧 环境配置

### 必需的环境变量
在 Vercel 项目设置中配置：

```bash
DEEPSEEK_API_KEY=sk-your-api-key-here
```

### 设置步骤
1. 访问 https://vercel.com/dashboard
2. 选择你的项目
3. 进入 **Settings** → **Environment Variables**
4. 添加 `DEEPSEEK_API_KEY`
5. 点击 **Save** 后 **Redeploy**

## 📊 与完整版后端的对比

| 功能 | 完整版 (backend/main.py) | Vercel 版 (api/index.py) |
|------|-------------------------|-------------------------|
| 聊天对话 | ✅ | ✅ |
| 流式输出 | ✅ | ✅ |
| PDF 上传 | ✅ | ✅ |
| TXT 上传 | ✅ | ✅ |
| DOCX 上传 | ✅ | ❌ |
| 网页爬取 | ✅ | ✅ |
| 音频转文字 | ✅ | ❌ |
| 思维导图 | ✅ | ❌ |
| 数据分析 | ✅ | ❌ |
| 测验生成 | ✅ | ❌ |
| 文件持久化 | ✅ | ❌ |

## 🚀 如果需要完整功能

如果你需要所有功能，需要：

### 方案 1: 购买服务器
- 阿里云/腾讯云/AWS 等云服务器
- 部署完整版后端 (`backend/main.py`)
- 配置 Nginx 反向代理
- 设置域名解析

### 方案 2: 混合部署
- **前端 + 基础 API**: Vercel（免费）
- **高级功能 API**: 单独的服务器
- 前端根据功能调用不同的后端

### 方案 3: 使用其他 Serverless 平台
- Railway.app（有免费额度）
- Render.com（有免费额度）
- 这些平台支持持久化存储和更长的执行时间

## 📝 当前可用的完整工作流

在 Vercel 部署版本中，你可以：

1. **文档问答**
   - 上传 PDF/TXT 文档
   - 选择文档作为上下文
   - 向 AI 提问

2. **网页内容分析**
   - 爬取网页内容
   - 将网页作为文档上下文
   - 基于网页内容提问

3. **多轮对话**
   - 连续对话
   - 保持上下文
   - 流式显示回复

## 🔗 部署地址

- **主域名**: https://www.sunnyding.cn
- **Vercel 域名**: https://axonaxontest11.vercel.app

## 💡 建议

如果你主要需要：
- ✅ **文档问答**：当前 Vercel 版本完全够用
- ✅ **网页爬取**：当前 Vercel 版本完全够用
- ✅ **基础 AI 对话**：当前 Vercel 版本完全够用

如果你需要：
- ❌ **音频处理**：需要服务器
- ❌ **数据分析**：需要服务器
- ❌ **思维导图**：需要服务器
- ❌ **测验生成**：需要服务器

**成本考虑**：
- Vercel 免费版：完全免费（有使用量限制）
- 最便宜的服务器：约 ¥30-50/月（阿里云学生机）

---

**更新时间**: 2025年12月30日
