📚 NotebookLLM 项目导览
════════════════════════════════════════════════════════════════

🎯 快速导航

【第一次使用？】
👉 阅读：QUICKSTART.md (5分钟快速开始)

【详细学习？】
👉 阅读：README.md (完整项目介绍)
👉 阅读：USAGE.md (详细使用教程)

【如何部署？】
👉 阅读：DEPLOYMENT.md (部署和配置指南)

【了解架构？】
👉 阅读：PROJECT_STRUCTURE.md (项目结构详解)
👉 阅读：CONFIG.md (配置参考)

【项目完成度？】
👉 阅读：COMPLETED.md (完成总结)

════════════════════════════════════════════════════════════════

📂 文件结构说明

root/
│
├─ 🎨 前端应用
│  ├─ frontend/
│  │  ├─ index.html          ← 完整的前端应用（HTML+CSS+JS）
│  │  └─ package.json        ← 项目配置
│  └─ 【无需额外依赖，直接打开或使用服务器】
│
├─ 🚀 后端应用  
│  ├─ backend/
│  │  ├─ main.py            ← 基础版本（推荐用于学习）
│  │  ├─ main_enhanced.py   ← 增强版本（多LLM支持）
│  │  ├─ requirements.txt    ← Python依赖列表
│  │  └─ .env.example       ← 环境变量模板
│  └─ 【需要：Python 3.8+】
│
├─ ⚡ 启动脚本
│  ├─ run_backend.bat       ← Windows后端启动
│  ├─ run_frontend.bat      ← Windows前端启动
│  ├─ run_backend.sh        ← Linux/macOS后端启动
│  └─ run_frontend.sh       ← Linux/macOS前端启动
│
└─ 📖 完整文档
   ├─ README.md             ← 项目主说明【必读】
   ├─ QUICKSTART.md         ← 30秒快速开始【快速上手】
   ├─ USAGE.md              ← 详细使用教程【深入学习】
   ├─ DEPLOYMENT.md         ← 部署指南【生产部署】
   ├─ CONFIG.md             ← 配置参考【自定义调整】
   ├─ PROJECT_STRUCTURE.md  ← 项目架构【理解原理】
   └─ COMPLETED.md          ← 完成总结【项目概览】

════════════════════════════════════════════════════════════════

🚀 最快开始（3步）

【Windows用户】
1️⃣  双击 run_backend.bat    (启动后端)
2️⃣  双击 run_frontend.bat   (启动前端，新开窗口)
3️⃣  浏览器打开 http://localhost:3000

【macOS/Linux用户】
1️⃣  ./run_backend.sh        (终端1启动后端)
2️⃣  ./run_frontend.sh       (终端2启动前端)
3️⃣  浏览器打开 http://localhost:3000

【验证安装】
✓ 前端: http://localhost:3000
✓ API:  http://localhost:8000/health
✓ 文档: http://localhost:8000/docs

════════════════════════════════════════════════════════════════

💡 主要特性

🎨 前端
  ✓ 紫色渐变现代设计
  ✓ 文件上传（拖拽/选择）
  ✓ 文本输入框
  ✓ 讨论参数配置
  ✓ 实时结果显示
  ✓ 完全响应式设计
  ✓ 零依赖（纯HTML/CSS/JS）

🚀 后端
  ✓ FastAPI高性能框架
  ✓ OpenAI API集成
  ✓ Anthropic Claude支持
  ✓ Swagger自动文档
  ✓ 异步处理
  ✓ 完整错误处理
  ✓ 多LLM支持

🤖 AI功能
  ✓ 自动生成讨论内容
  ✓ 自定义讨论深度
  ✓ 调整对话长度
  ✓ 选择语气风格
  ✓ 自定义讲者名称
  ✓ 智能解析输出

════════════════════════════════════════════════════════════════

📚 文档快速链接

根据您的需求选择文档：

【我是新手，想快速上手】
→ 阅读 QUICKSTART.md
  5分钟了解如何启动和使用应用

【我想全面了解这个项目】
→ 阅读 README.md
  包含功能介绍、API文档、配置说明等

【我想深入学习使用技巧】
→ 阅读 USAGE.md
  包含详细教程、最佳实践、常见场景示例

【我想在生产环境部署】
→ 阅读 DEPLOYMENT.md
  包含Docker部署、云服务部署、生产建议等

【我想自定义和扩展】
→ 阅读 CONFIG.md 和 PROJECT_STRUCTURE.md
  了解配置选项和项目架构

【我想看项目概览】
→ 阅读 COMPLETED.md
  了解已完成的功能和未来规划

════════════════════════════════════════════════════════════════

⚙️ 配置信息

API密钥：sk-5610a05204284964a0953677a117a9dd
前端地址：http://localhost:3000
后端地址：http://localhost:8000
API文档：http://localhost:8000/docs

════════════════════════════════════════════════════════════════

🔧 常见任务

【启动应用】
Windows:  run_backend.bat && run_frontend.bat
Linux:    ./run_backend.sh && ./run_frontend.sh

【安装依赖】
cd backend && pip install -r requirements.txt

【查看API文档】
访问 http://localhost:8000/docs

【修改API密钥】
编辑 backend/main.py 中的 API_KEY

【修改UI样式】
编辑 frontend/index.html 中的 <style>

【使用增强版本】
改为运行 python backend/main_enhanced.py

════════════════════════════════════════════════════════════════

🎯 使用场景示例

【学习复习】
- 输入：课程笔记
- 参数：深层讨论 + 教育启蒙
- 效果：师生讨论模式

【快速了解】
- 输入：新闻文章
- 参数：浅层讨论 + 轻松随意
- 效果：快速评论讨论

【商务分析】
- 输入：产品说明书
- 参数：中等讨论 + 专业严肃
- 效果：销售讨论模式

【创意启发】
- 输入：故事大纲
- 参数：深层讨论 + 娱乐幽默
- 效果：人物对话创意

════════════════════════════════════════════════════════════════

📞 需要帮助？

【常见问题】
→ 查看 README.md 中的故障排除部分
→ 查看 DEPLOYMENT.md 中的常见问题

【API相关】
→ 访问 http://localhost:8000/docs
→ 查看 README.md 中的API文档部分

【技术细节】
→ 查看 PROJECT_STRUCTURE.md
→ 查看代码注释

════════════════════════════════════════════════════════════════

✨ 项目亮点

1️⃣  完全功能 - 从文档到讨论的完整流程
2️⃣  即插即用 - 无需复杂配置，一键启动
3️⃣  文档齐全 - 6份详细文档，涵盖所有方面
4️⃣  易于部署 - 支持Windows/Mac/Linux/Docker/云服务
5️⃣  高度定制 - 支持多LLM，易于扩展

════════════════════════════════════════════════════════════════

🚀 立即开始！

选择一个文档开始探索：
【快速开始】→ QUICKSTART.md
【完整介绍】→ README.md
【详细教程】→ USAGE.md
【部署指南】→ DEPLOYMENT.md

祝您使用愉快！ 🎉

════════════════════════════════════════════════════════════════
最后更新：2024年12月30日
版本：v1.0.0 (完全功能版本)
════════════════════════════════════════════════════════════════
