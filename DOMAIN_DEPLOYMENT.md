# 域名部署指南 - sunnyding.cn

## 📋 部署概览

本指南将帮助您将 Axon AI Research Assistant 项目部署到域名 `sunnyding.cn`。

## 🎯 部署架构

```
用户浏览器
    ↓
sunnyding.cn (前端 - 静态文件)
    ↓
api.sunnyding.cn 或 sunnyding.cn/api (后端 API)
```

## 📦 部署前准备

### 1. 服务器要求
- **系统**: Linux (推荐 Ubuntu 20.04/22.04) 或 Windows Server
- **内存**: 至少 2GB RAM
- **CPU**: 至少 1核
- **存储**: 至少 10GB 可用空间
- **公网IP**: 需要一个固定的公网 IP 地址

### 2. 域名配置
在您的域名提供商（如阿里云、腾讯云等）配置 DNS 记录：

```
A 记录:
sunnyding.cn        →  您的服务器公网IP
www.sunnyding.cn    →  您的服务器公网IP

（可选）后端独立域名:
A 记录:
api.sunnyding.cn    →  您的服务器公网IP
```

### 3. 软件依赖
- **Web服务器**: Nginx (推荐) 或 Apache
- **Python**: 3.8+ (后端)
- **SSL证书**: Let's Encrypt (免费) 或付费证书

## 🚀 部署步骤

### 方案 A: 使用 Nginx (推荐)

#### 步骤 1: 安装 Nginx

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nginx -y
```

**CentOS/RHEL:**
```bash
sudo yum install epel-release -y
sudo yum install nginx -y
```

#### 步骤 2: 上传项目文件

使用 FTP、SCP 或 Git 将项目上传到服务器：

```bash
# 使用 Git 克隆（如果项目在 Git 仓库）
cd /var/www
sudo git clone <your-repo-url> axon

# 或使用 SCP 上传
scp -r ./mynotebookllmwebsite user@your-server-ip:/var/www/axon
```

#### 步骤 3: 配置前端

将前端文件放置到 Nginx 目录：

```bash
sudo mkdir -p /var/www/sunnyding.cn
sudo cp -r /path/to/frontend/* /var/www/sunnyding.cn/
sudo chown -R www-data:www-data /var/www/sunnyding.cn
sudo chmod -R 755 /var/www/sunnyding.cn
```

#### 步骤 4: 配置 Nginx

创建 Nginx 配置文件（参考 `nginx.conf` 文件）：

```bash
sudo nano /etc/nginx/sites-available/sunnyding.cn
```

使用本项目提供的 `nginx.conf` 配置（见下文），然后启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/sunnyding.cn /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

#### 步骤 5: 部署后端

```bash
cd /var/www/axon/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env  # 编辑配置
```

使用 Systemd 管理后端服务（参考 `axon-backend.service` 文件）：

```bash
sudo cp axon-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start axon-backend
sudo systemctl enable axon-backend
```

#### 步骤 6: 配置 SSL 证书

使用 Let's Encrypt 获取免费 SSL 证书：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d sunnyding.cn -d www.sunnyding.cn

# 自动续期
sudo certbot renew --dry-run
```

#### 步骤 7: 更新前端 API 地址

编辑前端 `index.html` 文件，更新 API 基础地址：

```javascript
const API_BASE_URL = 'https://sunnyding.cn/api';  // 或 'https://api.sunnyding.cn'
```

### 方案 B: 使用云服务部署

#### Vercel (前端静态托管)

1. 安装 Vercel CLI:
```bash
npm install -g vercel
```

2. 在 frontend 目录运行:
```bash
cd frontend
vercel --prod
```

3. 在 Vercel 控制台绑定域名 sunnyding.cn

4. 配置环境变量指向您的后端 API

#### 阿里云/腾讯云服务器

使用提供的部署脚本 `deploy.sh`：

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🔧 配置文件说明

### 前端配置
- `index.html`: 主页面，需要修改 API_BASE_URL
- `axon-icon.svg`: 网站图标

### 后端配置
- `backend/.env`: 环境变量配置
  ```
  DEEPSEEK_API_KEY=your_api_key_here
  API_BASE_URL=https://api.deepseek.com
  HOST=0.0.0.0
  PORT=8000
  ```

### Nginx 配置
- `nginx.conf`: Nginx 服务器配置
- `axon-backend.service`: Systemd 服务配置

## 🔍 验证部署

1. **检查 Nginx 状态**:
```bash
sudo systemctl status nginx
```

2. **检查后端服务**:
```bash
sudo systemctl status axon-backend
curl http://localhost:8000/health
```

3. **测试域名访问**:
```bash
curl https://sunnyding.cn
curl https://sunnyding.cn/api/health
```

4. **浏览器测试**:
   - 访问 https://sunnyding.cn
   - 测试上传文件功能
   - 测试问答功能
   - 测试笔记本下载

## 🛠️ 故障排查

### 502 Bad Gateway
- 检查后端服务是否运行: `sudo systemctl status axon-backend`
- 检查端口是否被占用: `sudo netstat -tlnp | grep 8000`
- 查看后端日志: `sudo journalctl -u axon-backend -f`

### CORS 错误
- 确保 Nginx 配置中包含正确的 CORS 头
- 检查前端 API_BASE_URL 配置是否正确

### 文件上传失败
- 检查 Nginx `client_max_body_size` 设置
- 确保后端 `upload_files/` 目录有写权限

### SSL 证书问题
- 检查证书是否过期: `sudo certbot certificates`
- 手动续期: `sudo certbot renew`

## 📊 监控和维护

### 日志位置
- **Nginx 访问日志**: `/var/log/nginx/access.log`
- **Nginx 错误日志**: `/var/log/nginx/error.log`
- **后端日志**: `sudo journalctl -u axon-backend -f`

### 定期维护
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 重启服务
sudo systemctl restart nginx
sudo systemctl restart axon-backend

# 清理旧日志
sudo find /var/log/nginx/ -name "*.log" -mtime +30 -delete
```

## 🔐 安全建议

1. **启用防火墙**:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

2. **定期更新依赖**:
```bash
cd /var/www/axon/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

3. **配置备份**:
   - 定期备份数据库和上传的文件
   - 备份配置文件

4. **监控资源使用**:
```bash
htop  # CPU/内存监控
df -h  # 磁盘空间
```

## 📞 支持

如果遇到问题，请检查：
1. 服务器日志
2. Nginx 配置
3. 防火墙规则
4. DNS 解析是否生效

## 🎉 完成

部署完成后，您应该能够通过 `https://sunnyding.cn` 访问您的 Axon AI Research Assistant！
