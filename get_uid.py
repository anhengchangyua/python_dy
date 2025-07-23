#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取微博用户UID的工具脚本
"""

import requests
import re
import json
from urllib.parse import urlparse, parse_qs

def get_uid_from_url(weibo_url):
    """从微博链接中提取UID"""
    try:
        # 处理不同格式的微博链接
        if 'weibo.com/u/' in weibo_url:
            # https://weibo.com/u/1234567890
            uid = weibo_url.split('/u/')[1].split('?')[0].split('/')[0]
            return uid
        elif 'weibo.com/' in weibo_url and '/u/' not in weibo_url:
            # https://weibo.com/username 需要进一步解析
            return get_uid_from_username_url(weibo_url)
        elif 'm.weibo.cn/u/' in weibo_url:
            # https://m.weibo.cn/u/1234567890
            uid = weibo_url.split('/u/')[1].split('?')[0].split('/')[0]
            return uid
        else:
            print("不支持的链接格式")
            return None
    except Exception as e:
        print(f"解析链接失败: {e}")
        return None

def get_uid_from_username_url(weibo_url):
    """从用户名链接获取UID"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(weibo_url, headers=headers, allow_redirects=True)
        
        # 查找UID
        uid_pattern = r'"oid":"(\d+)"'
        match = re.search(uid_pattern, response.text)
        if match:
            return match.group(1)
        
        # 尝试其他模式
        uid_pattern2 = r'CONFIG\[\'oid\'\]=\'(\d+)\''
        match2 = re.search(uid_pattern2, response.text)
        if match2:
            return match2.group(1)
            
        # 从重定向URL中获取
        if '/u/' in response.url:
            return get_uid_from_url(response.url)
            
        print("无法从页面中提取UID")
        return None
        
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def search_user_by_keyword(keyword):
    """通过关键词搜索用户"""
    try:
        search_url = f"https://m.weibo.cn/api/container/getIndex"
        params = {
            'containerid': f'100103type=1&q={keyword}',
            'page_type': 'searchall'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://m.weibo.cn'
        }
        
        response = requests.get(search_url, params=params, headers=headers)
        data = response.json()
        
        if data.get('ok') == 1:
            cards = data.get('data', {}).get('cards', [])
            users = []
            
            for card in cards:
                if card.get('card_type') == 10:  # 用户卡片
                    card_group = card.get('card_group', [])
                    for group in card_group:
                        if group.get('card_type') == 10:
                            user = group.get('user', {})
                            users.append({
                                'uid': user.get('id'),
                                'screen_name': user.get('screen_name'),
                                'description': user.get('description', ''),
                                'followers_count': user.get('followers_count', 0),
                                'verified': user.get('verified', False)
                            })
            
            return users
        else:
            print("搜索失败")
            return []
            
    except Exception as e:
        print(f"搜索用户失败: {e}")
        return []

def main():
    """主函数"""
    print("=== 微博用户UID获取工具 ===")
    print("1. 从微博链接获取UID")
    print("2. 通过用户名搜索")
    
    choice = input("请选择操作方式 (1/2): ").strip()
    
    if choice == '1':
        weibo_url = input("请输入微博用户链接: ").strip()
        if weibo_url:
            uid = get_uid_from_url(weibo_url)
            if uid:
                print(f"提取到的UID: {uid}")
            else:
                print("无法提取UID")
        else:
            print("链接不能为空")
    
    elif choice == '2':
        keyword = input("请输入用户名关键词: ").strip()
        if keyword:
            print("正在搜索用户...")
            users = search_user_by_keyword(keyword)
            
            if users:
                print(f"\n找到 {len(users)} 个用户:")
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user['screen_name']} (UID: {user['uid']})")
                    print(f"   简介: {user['description'][:50]}...")
                    print(f"   粉丝数: {user['followers_count']}")
                    print(f"   已认证: {'是' if user['verified'] else '否'}")
                    print()
            else:
                print("没有找到相关用户")
        else:
            print("关键词不能为空")
    
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
