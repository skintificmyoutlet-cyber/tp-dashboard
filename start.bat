@echo off
echo ========================================
echo TP投放数据看板 - 快速启动
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [OK] 依赖已安装
)

echo.
echo [2/3] 检查API配置...
if not exist credentials.json (
    if not exist service_account.json (
        echo [警告] 未找到 credentials.json 或 service_account.json
        echo.
        echo 请按照以下步骤配置：
        echo 1. 访问 https://console.cloud.google.com/
        echo 2. 创建项目并启用 Google Sheets API
        echo 3. 创建凭据（OAuth或Service Account）
        echo 4. 下载JSON文件到当前目录
        echo.
        echo 详细步骤请查看 README.md
        pause
        exit /b 1
    )
)

echo [OK] 找到API凭据
echo.
echo [3/3] 启动应用...
echo.
echo ========================================
echo 应用将在浏览器中打开
echo 地址: http://localhost:8501
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

streamlit run app.py
