#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博爬虫配置文件
"""

# 请求配置
REQUEST_CONFIG = {
    'timeout': 10,
    'retry_times': 3,
    'delay_range': (1, 3),  # 请求间隔范围（秒）
}

# 用户代理列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

# 微博API配置
WEIBO_CONFIG = {
    'base_url': 'https://m.weibo.cn',
    'api_url': 'https://m.weibo.cn/api/container/getIndex',
    'max_pages_per_request': 50,
    'default_container_prefix': '107603',
}

# 输出配置
OUTPUT_CONFIG = {
    'default_format': 'both',  # csv, json, both
    'encoding': 'utf-8-sig',
    'create_timestamp_dir': True,
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file_name': 'weibo_scraper.log',
}

# Selenium配置
SELENIUM_CONFIG = {
    'implicit_wait': 10,
    'page_load_timeout': 30,
    'window_size': (1920, 1080),
    'chrome_options': [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-blink-features=AutomationControlled',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
}
