# 部署到 sunnyding.cn - 文件说明

本目录包含将 Axon 项目部署到 sunnyding.cn 域名所需的所有配置文件和脚本。

## 📁 部署相关文件

### 📘 文档文件

1. **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** ⭐ 推荐首先阅读
   - 三步快速部署指南
   - 最简单的部署方式
   - 适合想要快速上线的用户

2. **[DOMAIN_DEPLOYMENT.md](DOMAIN_DEPLOYMENT.md)**
   - 完整详细的部署指南
   - 包含多种部署方案
   - 故障排查和维护说明
   - 适合需要深入理解的用户

3. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**
   - 部署前检查清单
   - 确保不遗漏任何步骤
   - 包含验证和测试步骤

### ⚙️ 配置文件

4. **[nginx.conf](nginx.conf)**
   - Nginx Web 服务器配置
   - 包含 SSL、CORS、代理等配置
   - 放置位置：`/etc/nginx/sites-available/sunnyding.cn`

5. **[axon-backend.service](axon-backend.service)**
   - Systemd 服务配置
   - 用于管理后端服务
   - 放置位置：`/etc/systemd/system/axon-backend.service`

6. **[frontend/config.js](frontend/config.js)**
   - 前端环境配置
   - 自动适配开发/生产环境
   - 无需手动修改

7. **[backend/.env.example](backend/.env.example)**
   - 后端环境变量模板
   - 复制为 `.env` 并填入实际配置

### 🚀 部署脚本

8. **[deploy.sh](deploy.sh)**
   - Linux/macOS 自动部署脚本
   - 一键完成所有部署步骤
   - 需要 root 权限

9. **[deploy.ps1](deploy.ps1)**
   - Windows Server PowerShell 部署脚本
   - 用于 Windows IIS 环境
   - 需要管理员权限

## 🎯 快速开始

### 方法 1: 自动部署（推荐）⭐

```bash
# 1. 上传项目到服务器
scp -r ./mynotebookllmwebsite user@your-server:/var/www/axon

# 2. SSH 登录服务器
ssh user@your-server

# 3. 运行部署脚本
cd /var/www/axon
chmod +x deploy.sh
sudo ./deploy.sh

# 4. 配置 API 密钥
sudo nano /var/www/axon/backend/.env
# 填入: DEEPSEEK_API_KEY=your_actual_key

# 5. 重启后端
sudo systemctl restart axon-backend

# 6. 访问网站
# https://sunnyding.cn
```

### 方法 2: 云服务托管

**Vercel (前端)**
```bash
cd frontend
vercel --prod
# 然后在 Vercel 控制台绑定域名
```

**阿里云/腾讯云**
- 使用云服务商提供的 Web 应用托管服务
- 参考各平台的部署文档

## 📋 部署架构

```
┌─────────────────────────────────────────┐
│         用户浏览器                        │
└───────────────┬─────────────────────────┘
                │
                │ HTTPS (443)
                ▼
┌─────────────────────────────────────────┐
│      Nginx (Web 服务器)                  │
│      sunnyding.cn                        │
│                                          │
│  ┌────────────┐      ┌──────────────┐  │
│  │  静态文件   │      │   /api 代理   │  │
│  │  (前端)    │      │              │  │
│  └────────────┘      └──────┬───────┘  │
└────────────────────────────┼───────────┘
                              │
                              │ HTTP (8000)
                              ▼
┌─────────────────────────────────────────┐
│      Python Backend                      │
│      FastAPI + DeepSeek API             │
│      localhost:8000                     │
└─────────────────────────────────────────┘
```

## 🔧 配置说明

### 1. DNS 配置

在域名提供商添加 A 记录：

| 主机记录 | 记录类型 | 记录值 |
|---------|---------|--------|
| @ | A | 服务器IP |
| www | A | 服务器IP |

### 2. 端口要求

| 端口 | 协议 | 用途 |
|------|------|------|
| 80 | HTTP | 自动重定向到 HTTPS |
| 443 | HTTPS | 网站访问 |
| 8000 | HTTP | 后端 API (内部) |

### 3. 环境变量

后端必需配置（`backend/.env`）：
```env
DEEPSEEK_API_KEY=your_api_key_here
API_BASE_URL=https://api.deepseek.com
HOST=0.0.0.0
PORT=8000
```

前端自动配置（`frontend/config.js`）：
- 开发环境：`http://localhost:8001/api`
- 生产环境：`/api` (通过 Nginx 代理)

## ✅ 验证部署

### 检查服务状态
```bash
# Nginx
sudo systemctl status nginx

# 后端
sudo systemctl status axon-backend

# 端口监听
sudo netstat -tlnp | grep -E ':(80|443|8000)'
```

### 测试 API
```bash
# 健康检查
curl http://localhost:8000/health
curl https://sunnyding.cn/api/health
```

### 浏览器测试
1. 访问 https://sunnyding.cn
2. 测试文件上传
3. 测试 AI 对话
4. 检查 SSL 证书

## 📊 日志位置

| 服务 | 日志路径 | 查看命令 |
|------|---------|---------|
| Nginx 访问 | `/var/log/nginx/sunnyding.cn.access.log` | `sudo tail -f /var/log/nginx/sunnyding.cn.access.log` |
| Nginx 错误 | `/var/log/nginx/sunnyding.cn.error.log` | `sudo tail -f /var/log/nginx/sunnyding.cn.error.log` |
| 后端服务 | systemd journal | `sudo journalctl -u axon-backend -f` |

## 🛠️ 常用命令

### 服务管理
```bash
# 重启 Nginx
sudo systemctl restart nginx

# 重启后端
sudo systemctl restart axon-backend

# 重新加载 Nginx 配置
sudo nginx -s reload

# 测试 Nginx 配置
sudo nginx -t
```

### SSL 证书
```bash
# 申请证书
sudo certbot --nginx -d sunnyding.cn -d www.sunnyding.cn

# 续期证书
sudo certbot renew

# 查看证书
sudo certbot certificates
```

### 更新代码
```bash
# 更新前端
cd /var/www/axon/frontend
sudo git pull  # 或上传新文件

# 更新后端
cd /var/www/axon/backend
sudo git pull  # 或上传新文件
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart axon-backend
```

## 🐛 故障排查

### 502 Bad Gateway
1. 检查后端是否运行
2. 检查防火墙规则
3. 查看后端日志

### 域名无法访问
1. 检查 DNS 解析
2. 检查防火墙端口
3. 检查 Nginx 状态

### SSL 证书错误
1. 确保域名已解析
2. 检查 80 端口可访问
3. 重新申请证书

详细排查方法见 [DOMAIN_DEPLOYMENT.md](DOMAIN_DEPLOYMENT.md)

## 📚 推荐阅读顺序

1. ✅ [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 确保准备就绪
2. 🚀 [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - 快速部署
3. 📖 [DOMAIN_DEPLOYMENT.md](DOMAIN_DEPLOYMENT.md) - 深入理解（可选）
4. 📋 [USAGE.md](USAGE.md) - 使用指南

## 💡 提示

- 🔐 保管好 API 密钥和服务器密码
- 📊 定期检查 API 使用量
- 🔄 定期更新系统和依赖包
- 💾 定期备份重要数据
- 📝 记录配置修改

## 🎉 部署成功

当一切就绪后，您的网站将在 https://sunnyding.cn 上线！

祝您部署顺利！ 🚀
