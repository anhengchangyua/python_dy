# 微博爬虫项目安装脚本 (PowerShell版)

Write-Host "=== 微博爬虫项目安装脚本 (PowerShell版) ===" -ForegroundColor Green
Write-Host ""

# 检查Python版本
try {
    $pythonVersion = python --version 2>$null
    Write-Host "检测到的Python版本: $pythonVersion" -ForegroundColor Blue
} catch {
    Write-Host "错误: 未找到Python，请先安装Python 3.7+" -ForegroundColor Red
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

# 检查是否存在虚拟环境
if (-not (Test-Path "venv")) {
    Write-Host "创建Python虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "错误: 创建虚拟环境失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit 1
    }
} else {
    Write-Host "虚拟环境已存在" -ForegroundColor Green
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# 升级pip
Write-Host "升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# 安装依赖
Write-Host "安装项目依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 安装依赖失败" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法：" -ForegroundColor Cyan
Write-Host "1. 激活虚拟环境: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. 运行快速入门: python quick_start.py" -ForegroundColor White
Write-Host "3. 获取用户UID: python get_uid.py" -ForegroundColor White
Write-Host "4. 开始抓取数据: python weibo_scraper.py" -ForegroundColor White
Write-Host ""
Write-Host "详细说明请查看 README.md 文件" -ForegroundColor Yellow
Write-Host ""

# 如果是直接运行脚本，暂停等待用户输入
if ($MyInvocation.InvocationName -ne '.') {
    Read-Host "按任意键退出"
}
