# NotebookLLM 后端启动脚本 (使用DeepSeek API)

Write-Host "========================================" -ForegroundColor Green
Write-Host "NotebookLLM 后端启动脚本" -ForegroundColor Green
Write-Host "LLM提供商: DeepSeek" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 检查Python
Write-Host "检查Python环境..." -ForegroundColor Yellow
python --version

# 进入后端目录
Push-Location backend

# 检查依赖
Write-Host ""
Write-Host "检查依赖包..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# 启动后端
Write-Host ""
Write-Host "启动后端服务器..." -ForegroundColor Green
Write-Host "API地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Redoc: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

python main.py

Pop-Location
