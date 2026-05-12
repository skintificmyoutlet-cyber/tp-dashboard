# TP投放数据看板

实时读取Google Sheets数据，生成交互式投放分析看板。

## 功能特性

- ✅ 实时读取Google Sheets数据
- ✅ 昨日数据 vs 前日对比
- ✅ 每周一自动切换上周汇总
- ✅ ID/MY/TH三市场切换
- ✅ FB+SP双渠道支持
- ✅ 交互式图表（Plotly）
- ✅ Top/Bottom素材排行
- ✅ 趋势分析

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置Google API

#### 方式A：OAuth授权（推荐）

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目（或选择现有项目）
3. 启用 **Google Sheets API**
   - 左侧菜单 → API和服务 → 启用API和服务
   - 搜索 "Google Sheets API" → 启用
4. 创建OAuth 2.0凭据
   - 左侧菜单 → API和服务 → 凭据
   - 点击 "创建凭据" → "OAuth客户端ID"
   - 应用类型选择 "桌面应用"
   - 下载JSON文件，重命名为 `credentials.json`
   - 放到 `tp_dashboard` 目录下

5. 首次运行会自动打开浏览器授权，授权后生成 `token.pickle`，以后无需再授权

### 3. 本地运行

```bash
cd tp_dashboard
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

### 4. 部署到云端（生成在线链接）

#### 使用Streamlit Cloud（免费）

1. 将代码推送到GitHub仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接GitHub仓库
4. 选择 `app.py` 作为主文件
5. 在 Secrets 中添加Google凭据（将 `credentials.json` 内容粘贴进去）
6. 部署完成后获得永久在线链接

## 数据源

Google Sheets ID: `1GvMIxMctcnJ1iAyRWqwEkjv_8F8pI-NdVRFLbdrf2C4`

### 表格结构

**FB广告数据**
- 表名：`FB广告-ID`, `FB广告-MY`, `FB广告-TH`
- 字段：date, account_id, campaign_name, adset_name, ad_name, spend, impressions, clicks, purchase_count, purchase_value, add_to_cart_count, add_to_cart_value

**SP广告数据**
- 表名：`SP广告-ID`, `SP广告-MY`, `SP广告-TH`
- 字段：Sequence, Ad Name, Status, Ads Type, Product ID, expense, ROAS, Direct ROAS, ACOS, Direct ACOS, Product Impressions, Product Clicks, Product CTR, country_name, run_date

## 使用说明

### 查看模式

- **昨日数据**：显示最新日期的数据，对比前一天
- **上周汇总**：每周一自动显示上周（周一到周日）的汇总数据

### 市场选择

- ID（印尼）
- MY（马来西亚）
- TH（泰国）

### 渠道选择

- FB（Facebook广告）
- SP（Shopee广告）

### 核心指标

**FB广告**
- 花费、转化金额、ROAS、购买次数
- 花费Top 10、转化Top 10
- 花费vs转化趋势图

**SP广告**
- 花费、平均ROAS、平均ACOS、总点击
- 花费Top 10、ROAS Top 10
- 花费趋势图

## 故障排查

### 授权失败

确保 `credentials.json` 文件格式正确，包含以下字段：
```json
{
  "installed": {
    "client_id": "...",
    "client_secret": "...",
    "redirect_uris": ["http://localhost"]
  }
}
```

### 数据加载失败

1. 检查Google Sheets权限（需要"任何人可查看"）
2. 检查表名是否正确（区分大小写）
3. 检查网络连接

### 部署到Streamlit Cloud

如果使用OAuth，需要在Streamlit Cloud的Secrets中添加：

```toml
[google]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
```

## 技术栈

- **Streamlit**: Web应用框架
- **Google Sheets API**: 数据读取
- **Plotly**: 交互式图表
- **Pandas**: 数据处理

## 更新日志

- 2026-05-12: 初始版本
  - 支持FB/SP双渠道
  - 支持ID/MY/TH三市场
  - 昨日数据+上周汇总
  - 交互式图表
