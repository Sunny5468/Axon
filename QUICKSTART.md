# 🚀 快速启动指南

## ⚡ 30秒快速开始

### Windows用户（最简单）

1. **启动后端**
   ```bash
   双击 run_backend.bat
   ```
   等待看到：`Uvicorn running on http://0.0.0.0:8000`

2. **启动前端** (新开一个命令行)
   ```bash
   双击 run_frontend.bat
   ```
   浏览器会自动打开：`http://localhost:3000`

3. **开始使用！**
   - 上传文件或输入文本
   - 配置讨论参数
   - 点击"生成讨论"

### macOS/Linux用户

```bash
# 终端1 - 启动后端
chmod +x run_backend.sh
./run_backend.sh

# 终端2 - 启动前端  
chmod +x run_frontend.sh
./run_frontend.sh
```

## 📋 安装依赖（仅第一次需要）

### Windows
```powershell
cd backend
pip install -r requirements.txt
```

### macOS/Linux
```bash
cd backend
pip3 install -r requirements.txt
```

## 🔑 配置API密钥

您的密钥已内置：`sk-5610a05204284964a0953677a117a9dd`

如需更换，编辑 `backend/main.py`：
```python
API_KEY = "sk-xxxx"  # 改为您的密钥
```

## ✅ 验证安装

打开浏览器访问：
- 前端：`http://localhost:3000` ✓
- 后端：`http://localhost:8000/health` ✓
- API文档：`http://localhost:8000/docs` ✓

## 🎯 测试示例

### 1. 简单文本测试

前端：
1. 选择"直接输入文本"
2. 粘贴：`Python是一种编程语言，具有简洁的语法和强大的功能。`
3. 点击"生成讨论"
4. 等待30秒左右看到结果

### 2. API测试（PowerShell）

```powershell
$url = "http://localhost:8000/api/generate"
$body = @{
    content = "人工智能的发展趋势"
    depth = "medium"
    length = "short"
    tone = "professional"
    speaker1 = "张教授"
    speaker2 = "李学生"
} | ConvertTo-Json

Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json"
```

## 🔧 常见问题

| 问题 | 解决 |
|------|------|
| 后端启动失败 | 检查Python版本 ≥3.8 |
| 前端无法连接 | 确保后端运行在8000端口 |
| API密钥错误 | 检查密钥是否正确配置 |
| 生成超时 | 减少讨论长度设置 |

## 📚 文档导航

- **[README.md](README.md)** - 项目介绍和API文档
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 详细部署指南
- **[USAGE.md](USAGE.md)** - 完整使用教程
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - 项目结构详解

## 🎨 前端功能

```
┌─────────────────────────────────────────────────┐
│       🎙️  NotebookLLM - AI讨论生成器             │
├──────────────────┬──────────────────────────────┤
│ 📝 上传文档      │ ⚙️  讨论设置                 │
│ ✏️  输入文本      │ • 深度、长度、语气           │
│ 📄 文件管理      │ • 讲者名称自定义             │
├────────────────────────────────────────────────┤
│               🎬 生成的讨论                      │
│  讲者1：发言内容...                             │
│  讲者2：发言内容...                             │
│  ...                                           │
└────────────────────────────────────────────────┘
```

## ⚙️ 后端端点

| 方法 | URL | 说明 |
|------|-----|------|
| GET | `/` | API主页 |
| GET | `/health` | 健康检查 |
| POST | `/api/generate` | **生成讨论** |
| GET | `/api/models` | 模型列表 |
| GET | `/docs` | Swagger文档 |

## 🚀 下一步

1. ✅ 启动应用
2. ✅ 测试基本功能
3. ✅ 根据需要调整参数
4. 📖 阅读[USAGE.md](USAGE.md)了解更多技巧
5. 🔧 查看[DEPLOYMENT.md](DEPLOYMENT.md)进行生产部署

## 💡 使用提示

- **最佳输入长度**: 50-500字
- **最快响应**: 使用gpt-3.5-turbo + 短篇设置
- **最佳质量**: 使用gpt-4 + 深层讨论设置
- **推荐组合**: 中等深度 + 中等长度 + 教育启蒙

## 🆘 遇到问题？

1. 检查[README.md](README.md)的故障排除部分
2. 查看后端控制台的错误信息
3. 打开浏览器F12查看前端错误
4. 访问`http://localhost:8000/docs`查看API完整文档

---

**现在就开始吧！** 🎉
