#!/bin/bash
# Axon 项目服务器部署脚本
# 服务器IP: 47.102.113.241
# 执行方式: bash deploy_server.sh

set -e  # 遇到错误立即退出

echo "================================================"
echo "  Axon 项目自动部署脚本"
echo "  开始时间: $(date)"
echo "================================================"

# 1. 更新系统
echo "[1/8] 更新系统软件包..."
apt update && apt upgrade -y

# 2. 安装基础工具
echo "[2/8] 安装基础工具..."
apt install -y git curl wget vim

# 3. 安装 Python 3.11
echo "[3/8] 安装 Python 3.11..."
apt install -y python3.11 python3.11-venv python3-pip

# 4. 安装 Nginx
echo "[4/8] 安装 Nginx..."
apt install -y nginx

# 5. 克隆项目
echo "[5/8] 克隆 GitHub 项目..."
cd /var/www
if [ -d "Axon" ]; then
    echo "项目已存在，拉取最新代码..."
    cd Axon
    git pull origin main
else
    git clone https://github.com/Sunny5468/Axon.git
    cd Axon
fi

# 6. 安装 Python 依赖
echo "[6/8] 安装 Python 依赖..."
cd /var/www/Axon/backend
pip3 install -r requirements.txt

# 7. 配置环境变量
echo "[7/8] 配置环境变量..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
DEEPSEEK_API_KEY=sk-229b5c8d1d6c4e0b8cffc3eb59679e60
EOF
    echo "环境变量配置完成"
else
    echo "环境变量文件已存在，跳过"
fi

# 8. 配置 Nginx
echo "[8/8] 配置 Nginx..."
cat > /etc/nginx/sites-available/axon << 'EOF'
server {
    listen 80;
    server_name sunnyding.cn www.sunnyding.cn 47.102.113.241;

    # 前端静态文件
    location / {
        root /var/www/Axon/frontend;
        try_files $uri $uri/ /index.html;
        index index.html;
    }

    # API 反向代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 支持流式响应
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        root /var/www/Axon/frontend;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/axon /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
nginx -t

# 重启 Nginx
systemctl restart nginx
systemctl enable nginx

echo "================================================"
echo "  基础环境部署完成！"
echo "================================================"
echo ""
echo "下一步操作："
echo "1. 启动后端服务: cd /var/www/Axon/backend && python3 main.py"
echo "2. 或使用 systemd 服务管理（推荐）"
echo ""
echo "访问地址："
echo "  - http://47.102.113.241"
echo "  - http://sunnyding.cn (需配置DNS解析)"
echo ""
