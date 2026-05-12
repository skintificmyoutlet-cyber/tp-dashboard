# 部署到Streamlit Cloud指南

## 方式一：使用GitHub + Streamlit Cloud（推荐）

### 步骤1：准备GitHub仓库

```bash
# 初始化git仓库
cd tp_dashboard
git init
git add .
git commit -m "Initial commit: TP投放数据看板"

# 创建GitHub仓库（在GitHub网站上创建）
# 然后推送代码
git remote add origin https://github.com/你的用户名/tp-dashboard.git
git branch -M main
git push -u origin main
```

### 步骤2：部署到Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择你的仓库：`你的用户名/tp-dashboard`
5. Main file path: `app.py`
6. 点击 "Advanced settings"

### 步骤3：配置Secrets

在 "Secrets" 中添加Google API凭据：

**方式A：使用OAuth（需要手动刷新token）**

将你的 `credentials.json` 内容复制粘贴：

```toml
[google_oauth]
client_id = "你的client_id.apps.googleusercontent.com"
project_id = "你的project_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_secret = "你的client_secret"
redirect_uris = ["http://localhost"]
```

**方式B：使用Service Account（推荐，自动化）**

1. 在Google Cloud Console创建Service Account
2. 下载JSON密钥
3. 将Google Sheets共享给Service Account邮箱（xxx@xxx.iam.gserviceaccount.com）
4. 在Secrets中添加：

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

### 步骤4：部署

点击 "Deploy" 按钮，等待部署完成（约2-3分钟）

部署成功后会得到一个永久链接：
```
https://你的用户名-tp-dashboard-xxxxx.streamlit.app
```

---

## 方式二：使用Heroku

### 步骤1：安装Heroku CLI

```bash
# Windows
# 下载安装：https://devcenter.heroku.com/articles/heroku-cli

# Mac
brew tap heroku/brew && brew install heroku
```

### 步骤2：创建Heroku应用

```bash
cd tp_dashboard
heroku login
heroku create tp-dashboard-你的名字
```

### 步骤3：添加配置文件

创建 `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

创建 `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

### 步骤4：部署

```bash
git add .
git commit -m "Add Heroku config"
git push heroku main
```

访问：`https://tp-dashboard-你的名字.herokuapp.com`

---

## 方式三：使用Railway

1. 访问 [railway.app](https://railway.app)
2. 连接GitHub仓库
3. 自动检测Streamlit应用
4. 部署完成

---

## 本地测试

在部署前，先本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 测试API配置
python test_setup.py

# 运行应用
streamlit run app.py
```

浏览器打开 `http://localhost:8501`

---

## 常见问题

### Q1: 部署后无法读取数据

**A:** 检查Google Sheets权限
- 确保表格设置为"任何人可查看"
- 或者将Service Account邮箱添加到共享列表

### Q2: Secrets配置错误

**A:** 确保TOML格式正确
- 字符串用双引号
- 私钥中的换行符用 `\n` 表示
- 不要有多余的空格

### Q3: 应用加载慢

**A:** 添加缓存
- 代码中已使用 `@st.cache_data(ttl=3600)`
- 数据会缓存1小时

### Q4: 如何更新数据

**A:** 
- 缓存会在1小时后自动刷新
- 或者点击右上角 "Rerun" 按钮手动刷新

---

## 推荐配置

**最佳实践：Service Account + Streamlit Cloud**

优点：
- ✅ 完全自动化，无需手动刷新token
- ✅ 免费托管
- ✅ 自动HTTPS
- ✅ 支持自定义域名
- ✅ 自动从GitHub更新

部署时间：约10分钟
维护成本：零

---

## 下一步

部署完成后，你可以：

1. 设置自定义域名（Streamlit Cloud支持）
2. 添加密码保护（使用 `streamlit-authenticator`）
3. 集成飞书/钉钉通知
4. 添加数据导出功能
5. 设置定时任务自动生成日报

需要帮助？随时问我！
