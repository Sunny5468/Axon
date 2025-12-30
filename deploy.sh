#!/bin/bash

# Axon 项目部署脚本 - sunnyding.cn
# 使用方法: chmod +x deploy.sh && ./deploy.sh

set -e  # 遇到错误立即退出

echo "================================================"
echo "  Axon 项目部署脚本"
echo "  域名: sunnyding.cn"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
DOMAIN="sunnyding.cn"
PROJECT_DIR="/var/www/axon"
FRONTEND_DIR="${PROJECT_DIR}/frontend"
BACKEND_DIR="${PROJECT_DIR}/backend"
NGINX_SITE_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}错误: 请使用 sudo 运行此脚本${NC}"
    echo "示例: sudo ./deploy.sh"
    exit 1
fi

echo -e "${GREEN}[1/10] 检查系统环境...${NC}"
# 检测系统类型
if [ -f /etc/debian_version ]; then
    PKG_MANAGER="apt"
    echo "检测到 Debian/Ubuntu 系统"
elif [ -f /etc/redhat-release ]; then
    PKG_MANAGER="yum"
    echo "检测到 CentOS/RHEL 系统"
else
    echo -e "${RED}不支持的操作系统${NC}"
    exit 1
fi

echo -e "${GREEN}[2/10] 更新系统软件包...${NC}"
if [ "$PKG_MANAGER" = "apt" ]; then
    apt update
else
    yum update -y
fi

echo -e "${GREEN}[3/10] 安装必要软件...${NC}"
if [ "$PKG_MANAGER" = "apt" ]; then
    apt install -y nginx python3 python3-pip python3-venv git curl
else
    yum install -y nginx python3 python3-pip git curl
fi

echo -e "${GREEN}[4/10] 创建项目目录...${NC}"
mkdir -p ${PROJECT_DIR}
mkdir -p ${FRONTEND_DIR}
mkdir -p ${BACKEND_DIR}

echo -e "${GREEN}[5/10] 复制项目文件...${NC}"
# 假设脚本在项目根目录运行
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r ${SCRIPT_DIR}/frontend/* ${FRONTEND_DIR}/
cp -r ${SCRIPT_DIR}/backend/* ${BACKEND_DIR}/

echo -e "${GREEN}[6/10] 配置后端环境...${NC}"
cd ${BACKEND_DIR}

# 创建虚拟环境
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 创建环境变量文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}创建 .env 配置文件...${NC}"
    cat > .env << EOF
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_api_key_here
API_BASE_URL=https://api.deepseek.com

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 文件上传配置
MAX_FILE_SIZE=104857600  # 100MB
UPLOAD_DIR=./upload_files

# 日志配置
LOG_LEVEL=INFO
EOF
    echo -e "${YELLOW}请编辑 ${BACKEND_DIR}/.env 文件，填入您的 API 密钥${NC}"
fi

deactivate

echo -e "${GREEN}[7/10] 配置 Nginx...${NC}"
# 复制 Nginx 配置
cp ${SCRIPT_DIR}/nginx.conf ${NGINX_SITE_DIR}/${DOMAIN}

# 创建符号链接
if [ ! -L "${NGINX_ENABLED_DIR}/${DOMAIN}" ]; then
    ln -s ${NGINX_SITE_DIR}/${DOMAIN} ${NGINX_ENABLED_DIR}/${DOMAIN}
fi

# 测试 Nginx 配置
nginx -t

echo -e "${GREEN}[8/10] 配置后端服务...${NC}"
# 复制 systemd 服务文件
cp ${SCRIPT_DIR}/axon-backend.service /etc/systemd/system/

# 重新加载 systemd
systemctl daemon-reload

# 启动并启用服务
systemctl enable axon-backend
systemctl start axon-backend

echo -e "${GREEN}[9/10] 配置 SSL 证书...${NC}"
if ! command -v certbot &> /dev/null; then
    echo "安装 Certbot..."
    if [ "$PKG_MANAGER" = "apt" ]; then
        apt install -y certbot python3-certbot-nginx
    else
        yum install -y certbot python3-certbot-nginx
    fi
fi

echo -e "${YELLOW}是否现在配置 SSL 证书? (y/n)${NC}"
read -p "输入选择: " setup_ssl

if [ "$setup_ssl" = "y" ] || [ "$setup_ssl" = "Y" ]; then
    echo -e "${YELLOW}正在获取 SSL 证书...${NC}"
    certbot --nginx -d ${DOMAIN} -d www.${DOMAIN}
    
    # 测试自动续期
    certbot renew --dry-run
else
    echo -e "${YELLOW}跳过 SSL 配置。稍后可以运行: sudo certbot --nginx -d ${DOMAIN}${NC}"
fi

echo -e "${GREEN}[10/10] 重启服务...${NC}"
systemctl restart nginx
systemctl restart axon-backend

echo ""
echo "================================================"
echo -e "${GREEN}  部署完成!${NC}"
echo "================================================"
echo ""
echo "访问地址:"
echo "  - HTTP:  http://${DOMAIN}"
echo "  - HTTPS: https://${DOMAIN}"
echo ""
echo "服务状态检查:"
echo "  - Nginx:  sudo systemctl status nginx"
echo "  - 后端:   sudo systemctl status axon-backend"
echo ""
echo "日志查看:"
echo "  - Nginx:  sudo tail -f /var/log/nginx/error.log"
echo "  - 后端:   sudo journalctl -u axon-backend -f"
echo ""
echo "重要提示:"
echo "  1. 请编辑 ${BACKEND_DIR}/.env 文件，配置您的 API 密钥"
echo "  2. 确保域名 DNS 已正确解析到服务器 IP"
echo "  3. 如果未配置 SSL，请运行: sudo certbot --nginx -d ${DOMAIN}"
echo ""
echo "================================================"
