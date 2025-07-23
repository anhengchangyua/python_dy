#!/bin/bash

# 微博爬虫项目安装脚本

echo "=== 微博爬虫项目安装脚本 ==="
echo

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "检测到的Python版本: $python_version"

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
else
    echo "虚拟环境已存在"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt

echo
echo "=== 安装完成 ==="
echo
echo "使用方法："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 运行快速入门: python quick_start.py"
echo "3. 获取用户UID: python get_uid.py"
echo "4. 开始抓取数据: python weibo_scraper.py"
echo
echo "详细说明请查看 README.md 文件"
echo
