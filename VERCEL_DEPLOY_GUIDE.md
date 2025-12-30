# 🚀 Vercel 免费部署指南 - sunnyding.cn

## ✨ 为什么选择 Vercel？

- 🆓 **完全免费** - 个人项目永久免费
- ⚡ **超快部署** - 5分钟上线
- 🌍 **全球CDN** - 自动加速
- 🔒 **自动HTTPS** - 免费SSL证书
- 🎯 **零配置** - 不需要服务器知识

---

## 📋 部署前准备

### ✅ 您已经拥有：
- ✅ 域名：sunnyding.cn
- ✅ 项目文件：完整的前后端代码
- ✅ Vercel 配置文件（已创建）

### 🔑 您还需要：
- [ ] GitHub 账号（免费注册）
- [ ] Vercel 账号（用 GitHub 登录，免费）
- [ ] DeepSeek API 密钥

---

## 🎯 部署步骤（图文详解）

### 第一步：准备 GitHub 账号

#### 1.1 注册 GitHub（如果还没有）

访问：https://github.com/signup

填写信息：
```
邮箱：您的邮箱
密码：设置密码
用户名：选择一个用户名
```

#### 1.2 验证邮箱

- 查看邮箱收到的验证邮件
- 点击验证链接

---

### 第二步：上传项目到 GitHub

#### 2.1 创建新仓库

1. 登录 GitHub
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   ```
   Repository name: axon-ai-assistant
   Description: AI Research Assistant powered by DeepSeek
   ☑️ Public（公开）
   ❌ 不要勾选 Add README
   ```
4. 点击 `Create repository`

#### 2.2 上传项目文件

**方法 A：使用 GitHub 网页版（最简单）**

1. 在新创建的仓库页面，点击 `uploading an existing file`
2. 拖拽整个项目文件夹到浏览器
3. 等待上传完成
4. 填写提交信息：`Initial commit`
5. 点击 `Commit changes`

**方法 B：使用 Git 命令行（推荐）**

在您当前的 PowerShell 中运行：

```powershell
# 进入项目目录
cd C:\Users\35696\mynotebookllmwebsite

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/axon-ai-assistant.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

如果提示输入用户名密码：
- 用户名：您的 GitHub 用户名
- 密码：GitHub Personal Access Token（不是登录密码）

**如何获取 Personal Access Token：**
1. GitHub 右上角头像 → Settings
2. 左侧菜单最下方 → Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token
5. 勾选 `repo` 权限
6. 复制生成的 token（只显示一次！）

---

### 第三步：部署到 Vercel

#### 3.1 注册 Vercel 账号

1. 访问：https://vercel.com/signup
2. 点击 **"Continue with GitHub"**（用 GitHub 登录）
3. 授权 Vercel 访问您的 GitHub

#### 3.2 导入项目

1. 进入 Vercel 控制台：https://vercel.com/new
2. 找到 `Import Git Repository`
3. 选择您刚才创建的仓库：`axon-ai-assistant`
4. 点击 `Import`

#### 3.3 配置项目

**Project Name:**（项目名称）
```
axon-ai-assistant
```

**Framework Preset:**（框架预设）
```
Other（保持默认）
```

**Root Directory:**（根目录）
```
./（保持默认）
```

**Build Command:**（构建命令）
```
留空（不需要构建）
```

**Output Directory:**（输出目录）
```
frontend
```

**Install Command:**（安装命令）
```
留空
```

#### 3.4 配置环境变量

点击 **"Environment Variables"** 展开：

添加环境变量：
```
Name:  DEEPSEEK_API_KEY
Value: 您的DeepSeek API密钥
```

**重要：** 勾选所有环境（Production, Preview, Development）

#### 3.5 开始部署

点击 **"Deploy"** 按钮

等待部署完成（通常 1-2 分钟）

---

### 第四步：绑定自定义域名

#### 4.1 在 Vercel 添加域名

1. 部署完成后，进入项目设置
2. 点击顶部菜单 **"Settings"**
3. 左侧菜单点击 **"Domains"**
4. 输入您的域名：`sunnyding.cn`
5. 点击 **"Add"**

#### 4.2 获取 DNS 配置信息

Vercel 会显示需要添加的 DNS 记录，例如：

```
类型: A
名称: @
值: 76.76.21.21

类型: CNAME
名称: www
值: cname.vercel-dns.com
```

**注意：** 实际的 IP 和 CNAME 值以 Vercel 显示的为准！

#### 4.3 在阿里云配置 DNS

1. 登录阿里云 DNS 控制台：https://dns.console.aliyun.com
2. 找到域名 `sunnyding.cn`
3. 点击 **"解析设置"**

**删除旧记录（如果有）：**
- 删除之前的 A 记录

**添加新记录：**

**记录 1：主域名**
```
记录类型：A
主机记录：@
解析线路：默认
记录值：76.76.21.21（以 Vercel 显示为准）
TTL：10分钟
```

**记录 2：www子域名**
```
记录类型：CNAME
主机记录：www
解析线路：默认
记录值：cname.vercel-dns.com（以 Vercel 显示为准）
TTL：10分钟
```

点击 **"确定"** 保存

#### 4.4 等待验证

- 返回 Vercel 控制台
- 等待域名验证（通常 5-30 分钟）
- 验证成功后会自动配置 HTTPS

---

## ✅ 验证部署

### 1. 检查 Vercel 默认域名

Vercel 会给您一个默认域名，例如：
```
https://axon-ai-assistant.vercel.app
```

在浏览器中访问，确保网站正常运行。

### 2. 检查自定义域名

等待 DNS 生效后（5-30分钟），访问：
```
https://sunnyding.cn
https://www.sunnyding.cn
```

### 3. 测试功能

- ✅ 页面能正常打开
- ✅ 可以发送消息
- ✅ AI 能正常回复
- ✅ HTTPS 小锁图标显示

---

## 🔍 常见问题

### Q1: Git 命令提示找不到？

**解决方法：**

下载安装 Git：https://git-scm.com/download/win

安装后重启 PowerShell

### Q2: git push 提示认证失败？

**解决方法：**

使用 Personal Access Token 而不是密码：

1. 生成 Token（见上文）
2. 使用 Token 作为密码

或者使用 GitHub Desktop（图形界面）：
https://desktop.github.com

### Q3: Vercel 部署失败？

**常见原因：**

1. **环境变量未设置** - 检查 DEEPSEEK_API_KEY 是否配置
2. **文件路径错误** - 确保 vercel.json 在项目根目录
3. **依赖问题** - 检查 api/requirements.txt 是否正确

**查看部署日志：**
- Vercel 项目页面 → Deployments
- 点击失败的部署 → 查看详细日志

### Q4: 域名配置后无法访问？

**检查步骤：**

1. **DNS 是否生效**
   ```powershell
   nslookup sunnyding.cn
   ```
   应该显示 Vercel 的 IP

2. **清除 DNS 缓存**
   ```powershell
   ipconfig /flushdns
   ```

3. **等待更长时间** - DNS 传播可能需要 24 小时

### Q5: API 调用失败？

**检查：**

1. DeepSeek API 密钥是否正确
2. 账户是否有余额
3. 查看 Vercel 函数日志：
   - 项目 → Functions → 查看日志

---

## 🎨 自定义配置

### 修改网站标题和图标

编辑 `frontend/index.html`：

```html
<title>您的网站名称</title>
<link rel="icon" href="/frontend/your-icon.svg">
```

提交到 GitHub，Vercel 会自动重新部署。

### 添加自定义域名邮箱

可以使用 Cloudflare Email Routing（免费）为您的域名配置邮箱：
- 例如：admin@sunnyding.cn

---

## 📊 Vercel 免费额度

| 项目 | 免费额度 | 说明 |
|------|---------|------|
| 带宽 | 100GB/月 | 足够个人使用 |
| 函数调用 | 100GB-小时/月 | API 调用次数 |
| 构建时长 | 6000分钟/月 | 重新部署次数 |
| 并发请求 | 1000 | 同时访问人数 |

超出额度后会提示升级，但个人项目基本不会超。

---

## 🔄 更新网站

### 方法 1：通过 Git（推荐）

```powershell
# 修改文件后
git add .
git commit -m "更新说明"
git push
```

Vercel 会自动检测并重新部署。

### 方法 2：直接在 GitHub 网页编辑

1. 进入 GitHub 仓库
2. 点击要编辑的文件
3. 点击铅笔图标编辑
4. 提交更改

Vercel 自动部署。

---

## 🎯 下一步

部署成功后，您可以：

1. ✅ 分享网站链接给朋友
2. ✅ 在社交媒体推广
3. ✅ 监控网站访问情况（Vercel Analytics）
4. ✅ 继续开发新功能

---

## 📞 需要帮助？

如果遇到问题：

1. **查看 Vercel 文档**：https://vercel.com/docs
2. **查看部署日志**：Vercel 控制台 → Deployments
3. **提供以下信息寻求帮助**：
   - 错误截图
   - 部署日志
   - 具体报错信息

---

## 🎉 恭喜！

按照这个教程，您的网站应该已经成功部署到：

- ✅ Vercel 默认域名：`https://axon-ai-assistant.vercel.app`
- ✅ 自定义域名：`https://sunnyding.cn`

享受您的 AI 助手吧！🚀

---

**部署时间**: 2025年12月30日  
**部署平台**: Vercel  
**域名**: sunnyding.cn  
**状态**: ✅ 准备就绪
