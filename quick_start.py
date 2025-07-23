#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博爬虫快速入门示例
演示基本使用方法
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_scraper import WeiboScraper
import json

def demo_basic_usage():
    """演示基本使用方法"""
    print("=== 微博爬虫快速入门示例 ===\n")
    
    # 创建爬虫实例
    scraper = WeiboScraper()
    
    # 示例UID（这是一个公开的测试UID，实际使用时请替换）
    demo_uid = "1234567890"
    
    print("注意：这是一个演示脚本，使用的是示例UID。")
    print("实际使用时，请按照以下步骤：\n")
    
    print("1. 使用 get_uid.py 获取真实的用户UID")
    print("   python get_uid.py")
    print()
    
    print("2. 使用基础爬虫抓取数据")
    print("   python weibo_scraper.py")
    print()
    
    print("3. 使用Selenium爬虫（适用于复杂情况）")
    print("   python weibo_selenium_scraper.py")
    print()
    
    print("4. 批量抓取多个用户")
    print("   python batch_scraper.py")
    print()
    
    # 演示获取用户信息（这会失败，因为是示例UID）
    print("正在尝试获取用户信息...")
    try:
        user_info = scraper.get_user_info(demo_uid)
        if user_info:
            print(f"用户信息获取成功: {json.dumps(user_info, ensure_ascii=False, indent=2)}")
        else:
            print("❌ 用户信息获取失败（这是预期的，因为使用的是示例UID）")
    except Exception as e:
        print(f"❌ 获取用户信息时出错: {e}")
    
    print("\n=== 重要提示 ===")
    print("1. 请遵守微博的使用条款和robots.txt")
    print("2. 不要过于频繁地请求，避免对服务器造成压力")
    print("3. 仅用于学习和研究目的")
    print("4. 如遇到验证码或IP封禁，请降低抓取频率")
    print("\n详细使用说明请参考 README.md 文件")

def show_project_structure():
    """显示项目结构"""
    print("\n=== 项目文件结构 ===")
    files = [
        "weibo_scraper.py - 基础API爬虫（推荐）",
        "weibo_selenium_scraper.py - Selenium爬虫（高级）",
        "get_uid.py - UID获取工具",
        "batch_scraper.py - 批量抓取工具",
        "config.py - 配置文件",
        "requirements.txt - 依赖包列表",
        "README.md - 详细使用说明",
        "user_list_example.txt - 用户列表示例"
    ]
    
    for file_desc in files:
        print(f"  {file_desc}")

if __name__ == "__main__":
    demo_basic_usage()
    show_project_structure()
