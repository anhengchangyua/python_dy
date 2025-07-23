@echo off
chcp 65001 >nul
echo === 微博爬虫项目安装脚本 (Windows版) ===
echo.

REM 检查Python版本
echo 检测Python版本...
python --version 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
) else (
    echo 虚拟环境已存在
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)

echo.
echo === 安装完成 ===
echo.
echo 使用方法：
echo 1. 激活虚拟环境: venv\Scripts\activate.bat
echo 2. 运行快速入门: python quick_start.py
echo 3. 获取用户UID: python get_uid.py
echo 4. 开始抓取数据: python weibo_scraper.py
echo.
echo 详细说明请查看 README.md 文件
echo.
pause
