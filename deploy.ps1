# PowerShell 部署脚本 - Windows Server
# 使用方法: .\deploy.ps1

param(
    [string]$Domain = "sunnyding.cn",
    [string]$InstallPath = "C:\inetpub\axon"
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Axon 项目部署脚本 (Windows Server)" -ForegroundColor Cyan
Write-Host "  域名: $Domain" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "错误: 请以管理员身份运行此脚本" -ForegroundColor Red
    Write-Host "右键点击 PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/8] 检查 IIS 安装..." -ForegroundColor Green
$iisFeature = Get-WindowsFeature -Name Web-Server
if (-not $iisFeature.Installed) {
    Write-Host "安装 IIS..." -ForegroundColor Yellow
    Install-WindowsFeature -Name Web-Server -IncludeManagementTools
} else {
    Write-Host "IIS 已安装" -ForegroundColor Green
}

Write-Host "[2/8] 检查 Python 安装..." -ForegroundColor Green
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "错误: 未找到 Python。请先安装 Python 3.8 或更高版本" -ForegroundColor Red
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version
Write-Host "Python 版本: $pythonVersion" -ForegroundColor Green

Write-Host "[3/8] 创建项目目录..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallPath\frontend" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallPath\backend" | Out-Null

Write-Host "[4/8] 复制项目文件..." -ForegroundColor Green
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Path "$scriptDir\frontend\*" -Destination "$InstallPath\frontend\" -Recurse -Force
Copy-Item -Path "$scriptDir\backend\*" -Destination "$InstallPath\backend\" -Recurse -Force

Write-Host "[5/8] 配置后端环境..." -ForegroundColor Green
Set-Location "$InstallPath\backend"

# 创建虚拟环境
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# 激活虚拟环境并安装依赖
& ".\venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt

# 创建环境变量文件
if (-not (Test-Path ".env")) {
    Write-Host "创建 .env 配置文件..." -ForegroundColor Yellow
    @"
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_api_key_here
API_BASE_URL=https://api.deepseek.com

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 文件上传配置
MAX_FILE_SIZE=104857600
UPLOAD_DIR=./upload_files

# 日志配置
LOG_LEVEL=INFO
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "请编辑 $InstallPath\backend\.env 文件，填入您的 API 密钥" -ForegroundColor Yellow
}

deactivate

Write-Host "[6/8] 配置 IIS 网站..." -ForegroundColor Green

# 导入 IIS 模块
Import-Module WebAdministration

# 创建应用程序池
$appPoolName = "AxonAppPool"
if (-not (Test-Path "IIS:\AppPools\$appPoolName")) {
    New-WebAppPool -Name $appPoolName
    Set-ItemProperty "IIS:\AppPools\$appPoolName" -Name managedRuntimeVersion -Value ""
}

# 创建网站
$siteName = "Axon"
if (Get-Website -Name $siteName -ErrorAction SilentlyContinue) {
    Remove-Website -Name $siteName
}

New-Website -Name $siteName -PhysicalPath "$InstallPath\frontend" -ApplicationPool $appPoolName -Port 80 -HostHeader $Domain

# 添加绑定
New-WebBinding -Name $siteName -Protocol "http" -Port 80 -HostHeader "www.$Domain"

Write-Host "[7/8] 配置 URL Rewrite..." -ForegroundColor Green
Write-Host "请手动安装 URL Rewrite 模块:" -ForegroundColor Yellow
Write-Host "下载地址: https://www.iis.net/downloads/microsoft/url-rewrite" -ForegroundColor Yellow

Write-Host "[8/8] 创建后端服务启动脚本..." -ForegroundColor Green
$startBackendScript = @"
@echo off
cd /d $InstallPath\backend
call venv\Scripts\activate.bat
python main.py
"@
$startBackendScript | Out-File -FilePath "$InstallPath\start_backend.bat" -Encoding ASCII

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  部署完成!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "后续步骤:" -ForegroundColor Yellow
Write-Host "  1. 配置 DNS: 将 $Domain 指向服务器 IP" -ForegroundColor White
Write-Host "  2. 编辑 API 配置: $InstallPath\backend\.env" -ForegroundColor White
Write-Host "  3. 启动后端: 运行 $InstallPath\start_backend.bat" -ForegroundColor White
Write-Host "  4. 配置 SSL: 使用 Win-ACME 或其他工具获取证书" -ForegroundColor White
Write-Host ""
Write-Host "访问地址: http://$Domain" -ForegroundColor Green
Write-Host ""
