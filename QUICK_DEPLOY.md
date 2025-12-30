# 快速部署到 sunnyding.cn

## 🚀 三步部署

### 步骤 1: 准备服务器

确保您的服务器满足以下要求：
- ✅ 有公网 IP 地址
- ✅ 域名 sunnyding.cn 已解析到服务器 IP
- ✅ 开放 80 和 443 端口

### 步骤 2: 上传项目文件

使用以下任一方式上传项目到服务器：

**方式 A: 使用 SCP**
```bash
# Windows PowerShell
scp -r C:\Users\35696\mynotebookllmwebsite user@your-server-ip:/tmp/axon

# 登录服务器后
sudo mv /tmp/axon /var/www/axon
```

**方式 B: 使用 Git**
```bash
ssh user@your-server-ip
cd /var/www
sudo git clone <your-repo-url> axon
```

**方式 C: 使用 FTP 工具**
- 使用 FileZilla、WinSCP 等工具
- 上传整个项目文件夹到服务器

### 步骤 3: 运行自动部署脚本

登录服务器后：

```bash
cd /var/www/axon
chmod +x deploy.sh
sudo ./deploy.sh
```

部署脚本会自动：
1. ✅ 安装 Nginx
2. ✅ 安装 Python 依赖
3. ✅ 配置 Nginx
4. ✅ 配置后端服务
5. ✅ 申请 SSL 证书
6. ✅ 启动所有服务

---

## 📋 手动部署（可选）

如果您想手动控制每一步，参考 [DOMAIN_DEPLOYMENT.md](DOMAIN_DEPLOYMENT.md) 完整指南。

---

## ✅ 验证部署

部署完成后，执行以下检查：

### 1. 检查服务状态
```bash
# 检查 Nginx
sudo systemctl status nginx

# 检查后端
sudo systemctl status axon-backend
```

### 2. 测试 API
```bash
# 健康检查
curl http://localhost:8000/health

# 从外部访问
curl https://sunnyding.cn/api/health
```

### 3. 浏览器测试
打开浏览器访问：https://sunnyding.cn

测试以下功能：
- ✅ 上传文档
- ✅ 提问对话
- ✅ 生成音频
- ✅ 数据分析
- ✅ 思维导图

---

## 🔧 配置 API 密钥

部署完成后，**必须**配置 DeepSeek API 密钥：

```bash
# 编辑环境配置
sudo nano /var/www/axon/backend/.env

# 修改以下内容
DEEPSEEK_API_KEY=your_actual_api_key_here

# 重启后端服务
sudo systemctl restart axon-backend
```

---

## 🌐 DNS 配置参考

在您的域名提供商（如阿里云、腾讯云）添加以下 DNS 记录：

| 类型 | 主机记录 | 记录值 | TTL |
|------|---------|--------|-----|
| A | @ | 您的服务器IP | 600 |
| A | www | 您的服务器IP | 600 |

等待 DNS 生效（通常 5-30 分钟）

验证 DNS：
```bash
# Windows
nslookup sunnyding.cn

# Linux/Mac
dig sunnyding.cn
```

---

## 🔒 SSL 证书

部署脚本会自动使用 Let's Encrypt 申请免费 SSL 证书。

手动申请（如果自动失败）：
```bash
sudo certbot --nginx -d sunnyding.cn -d www.sunnyding.cn
```

证书自动续期：
```bash
# 测试续期
sudo certbot renew --dry-run

# Certbot 会自动设置 cron 任务进行续期
```

---

## 📊 查看日志

### Nginx 日志
```bash
# 访问日志
sudo tail -f /var/log/nginx/sunnyding.cn.access.log

# 错误日志
sudo tail -f /var/log/nginx/sunnyding.cn.error.log
```

### 后端日志
```bash
sudo journalctl -u axon-backend -f
```

---

## 🛠️ 常见问题

### 502 Bad Gateway
```bash
# 检查后端是否运行
sudo systemctl status axon-backend

# 重启后端
sudo systemctl restart axon-backend

# 查看错误
sudo journalctl -u axon-backend -n 50
```

### 域名无法访问
1. 检查 DNS 是否生效：`nslookup sunnyding.cn`
2. 检查防火墙：`sudo ufw status`
3. 检查 Nginx：`sudo nginx -t && sudo systemctl status nginx`

### 文件上传失败
```bash
# 检查上传目录权限
sudo chown -R www-data:www-data /var/www/axon/backend/upload_files
sudo chmod -R 755 /var/www/axon/backend/upload_files
```

### SSL 证书失败
确保：
- 域名已正确解析到服务器 IP
- 80 端口可以访问
- 服务器可以访问外网

---

## 🎉 完成！

现在您可以通过 https://sunnyding.cn 访问您的 Axon AI Research Assistant！

## 📧 需要帮助？

查看详细文档：
- [完整部署指南](DOMAIN_DEPLOYMENT.md)
- [Nginx 配置说明](nginx.conf)
- [环境配置](frontend/config.js)
