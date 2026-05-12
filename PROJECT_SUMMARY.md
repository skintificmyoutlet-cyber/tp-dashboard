# 🎉 TP投放数据看板 - 项目完成

## 📦 已创建文件

```
tp_dashboard/
├── app.py                          # 主应用（Streamlit看板）
├── google_sheets_reader.py         # Google Sheets API读取模块
├── requirements.txt                # Python依赖
├── test_setup.py                   # API配置测试脚本
├── start.bat                       # Windows快速启动脚本
├── README.md                       # 使用说明
├── DEPLOY.md                       # 部署指南
├── credentials_template.txt        # OAuth凭据模板
├── .gitignore                      # Git忽略文件
├── .streamlit/
│   ├── config.toml                # Streamlit配置
│   └── secrets.toml.example       # Secrets配置示例
```

## ✨ 核心功能

### 1. 数据读取
- ✅ 实时读取Google Sheets数据
- ✅ 支持3种认证方式：
  - OAuth 2.0（本地开发）
  - Service Account（云端部署）
  - Streamlit Secrets（自动识别）

### 2. 数据分析
- ✅ **昨日数据**：最新日期数据 + 日环比
- ✅ **上周汇总**：每周一自动切换到上周数据
- ✅ **市场切换**：ID/MY/TH三市场
- ✅ **渠道切换**：FB/SP双渠道

### 3. 可视化
- ✅ 核心指标卡片（花费、转化、ROAS等）
- ✅ Top 10 广告排行（花费/转化/ROAS）
- ✅ 趋势图表（Plotly交互式）
- ✅ 原始数据表格

### 4. 部署方式
- ✅ 本地运行（localhost:8501）
- ✅ Streamlit Cloud（免费在线链接）
- ✅ Heroku
- ✅ Railway

## 🚀 快速开始

### 本地运行（3步）

**步骤1：安装依赖**
```bash
cd tp_dashboard
pip install -r requirements.txt
```

**步骤2：配置Google API**

选择以下任一方式：

**方式A：OAuth（推荐本地开发）**
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建项目 → 启用 Google Sheets API
3. 创建 OAuth 2.0 凭据（桌面应用）
4. 下载JSON → 重命名为 `credentials.json`
5. 放到 `tp_dashboard` 目录

**方式B：Service Account（推荐云端部署）**
1. 在Google Cloud Console创建Service Account
2. 下载JSON → 重命名为 `service_account.json`
3. 将Google Sheets共享给Service Account邮箱
4. 放到 `tp_dashboard` 目录

**步骤3：启动应用**

Windows:
```bash
start.bat
```

Mac/Linux:
```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`

### 测试配置

运行测试脚本验证API配置：
```bash
python test_setup.py
```

## 🌐 部署到云端（生成在线链接）

### 推荐：Streamlit Cloud（免费）

**步骤1：推送到GitHub**
```bash
cd tp_dashboard
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/tp-dashboard.git
git push -u origin main
```

**步骤2：部署**
1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 连接GitHub仓库
3. 选择 `app.py`
4. 在Secrets中添加Service Account凭据（参考 `.streamlit/secrets.toml.example`）
5. 点击Deploy

**步骤3：获取链接**
部署完成后得到永久链接：
```
https://你的用户名-tp-dashboard-xxxxx.streamlit.app
```

详细步骤见 [DEPLOY.md](DEPLOY.md)

## 📊 使用说明

### 界面操作

1. **选择市场**：ID（印尼）/ MY（马来西亚）/ TH（泰国）
2. **选择渠道**：FB（Facebook）/ SP（Shopee）
3. **查看模式**：
   - 昨日数据：显示最新日期 + 日环比
   - 上周汇总：显示上周一到周日的汇总

### 核心指标

**FB广告**
- 花费、转化金额、ROAS、购买次数
- 花费Top 10、转化Top 10
- 花费vs转化趋势

**SP广告**
- 花费、平均ROAS、平均ACOS、总点击
- 花费Top 10、ROAS Top 10
- 花费趋势

### 数据刷新

- 数据缓存1小时自动刷新
- 手动刷新：点击右上角 "⋮" → "Rerun"

## 🔧 技术栈

- **Streamlit** - Web应用框架
- **Google Sheets API** - 数据源
- **Plotly** - 交互式图表
- **Pandas** - 数据处理

## 📝 下一步优化

可以继续添加的功能：

1. **密码保护**
   ```bash
   pip install streamlit-authenticator
   ```

2. **数据导出**
   - 导出Excel/CSV
   - 生成PDF报告

3. **飞书/钉钉集成**
   - 自动推送日报
   - 异常数据告警

4. **更多图表**
   - 漏斗分析
   - 同期对比
   - 产品维度分析

5. **定时任务**
   - 每天自动生成日报
   - 每周一自动生成周报

需要这些功能随时告诉我！

## ❓ 常见问题

### Q1: 首次运行报错 "未找到credentials.json"
**A:** 需要先配置Google API凭据，参考上面"配置Google API"部分

### Q2: 数据显示为空
**A:** 检查：
1. Google Sheets权限（需要"任何人可查看"或共享给Service Account）
2. 表名是否正确（区分大小写）
3. 数据格式是否正确

### Q3: 部署后无法访问
**A:** 
1. 确保Secrets配置正确
2. 检查Service Account权限
3. 查看Streamlit Cloud日志

### Q4: 如何更新代码
**A:** 
```bash
git add .
git commit -m "Update"
git push
```
Streamlit Cloud会自动重新部署

## 📞 需要帮助？

遇到问题随时问我！我可以帮你：
- 调试错误
- 添加新功能
- 优化性能
- 定制化开发

---

**项目状态：✅ 已完成，可以开始使用！**

下一步：
1. 运行 `python test_setup.py` 测试配置
2. 运行 `streamlit run app.py` 本地预览
3. 部署到Streamlit Cloud获取在线链接
