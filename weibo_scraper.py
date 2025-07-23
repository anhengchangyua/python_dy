#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博用户作品数据爬虫
支持抓取指定用户的所有微博内容、点赞数、转发数、评论数等信息
"""

import requests
import json
import time
import re
import pandas as pd
from urllib.parse import urlencode, quote
from fake_useragent import UserAgent
import logging
from datetime import datetime
import os

class WeiboScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.chrome,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://m.weibo.cn/',
        }
        self.session.headers.update(self.headers)
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('weibo_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_user_info(self, uid):
        """获取用户基本信息"""
        url = f"https://m.weibo.cn/api/container/getIndex"
        params = {
            'type': 'uid',
            'value': uid,
            'containerid': f'100505{uid}'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('ok') == 1:
                userinfo = data.get('data', {}).get('userInfo', {})
                return {
                    'uid': userinfo.get('id'),
                    'screen_name': userinfo.get('screen_name'),
                    'followers_count': userinfo.get('followers_count'),
                    'follow_count': userinfo.get('follow_count'),
                    'statuses_count': userinfo.get('statuses_count'),
                    'description': userinfo.get('description'),
                    'verified': userinfo.get('verified'),
                    'verified_reason': userinfo.get('verified_reason', '')
                }
        except Exception as e:
            self.logger.error(f"获取用户信息失败: {e}")
            return None
    
    def get_user_weibo_list(self, uid, max_pages=10):
        """获取用户微博列表"""
        weibos = []
        containerid = f'107603{uid}'
        
        for page in range(1, max_pages + 1):
            self.logger.info(f"正在抓取第 {page} 页微博...")
            
            url = "https://m.weibo.cn/api/container/getIndex"
            params = {
                'type': 'uid',
                'value': uid,
                'containerid': containerid,
                'page': page
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get('ok') != 1:
                    self.logger.warning(f"第 {page} 页请求失败")
                    break
                
                cards = data.get('data', {}).get('cards', [])
                if not cards:
                    self.logger.info(f"第 {page} 页没有更多数据")
                    break
                
                for card in cards:
                    if card.get('card_type') == 9:  # 微博卡片
                        mblog = card.get('mblog')
                        if mblog:
                            weibo_data = self.parse_weibo_data(mblog)
                            if weibo_data:
                                weibos.append(weibo_data)
                
                # 添加延时避免被封
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"抓取第 {page} 页失败: {e}")
                continue
        
        return weibos
    
    def parse_weibo_data(self, mblog):
        """解析微博数据"""
        try:
            # 清理文本内容
            text = mblog.get('text', '')
            text_raw = mblog.get('text_raw', '')
            
            # 移除HTML标签
            text_clean = re.sub(r'<[^>]+>', '', text)
            
            # 获取图片链接
            pics = []
            if mblog.get('pics'):
                pics = [pic.get('large', {}).get('url', '') for pic in mblog.get('pics', [])]
            
            # 获取视频链接
            video_url = ''
            if mblog.get('page_info', {}).get('type') == 'video':
                video_url = mblog.get('page_info', {}).get('urls', {}).get('mp4_720p_mp4', '')
            
            # 转发微博信息
            retweeted_status = None
            if mblog.get('retweeted_status'):
                retweeted_status = {
                    'text': re.sub(r'<[^>]+>', '', mblog.get('retweeted_status', {}).get('text', '')),
                    'user_name': mblog.get('retweeted_status', {}).get('user', {}).get('screen_name', ''),
                    'created_at': mblog.get('retweeted_status', {}).get('created_at', '')
                }
            
            return {
                'id': mblog.get('id'),
                'created_at': mblog.get('created_at'),
                'text': text_clean,
                'text_raw': text_raw,
                'source': mblog.get('source', ''),
                'reposts_count': mblog.get('reposts_count', 0),
                'comments_count': mblog.get('comments_count', 0),
                'attitudes_count': mblog.get('attitudes_count', 0),
                'pics': pics,
                'video_url': video_url,
                'retweeted_status': retweeted_status,
                'user_id': mblog.get('user', {}).get('id'),
                'user_name': mblog.get('user', {}).get('screen_name', ''),
                'scheme': mblog.get('scheme', ''),
                'mblogtype': mblog.get('mblogtype', 0)
            }
            
        except Exception as e:
            self.logger.error(f"解析微博数据失败: {e}")
            return None
    
    def save_to_csv(self, data, filename):
        """保存数据到CSV文件"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            self.logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            self.logger.error(f"保存CSV文件失败: {e}")
    
    def save_to_json(self, data, filename):
        """保存数据到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            self.logger.error(f"保存JSON文件失败: {e}")
    
    def scrape_user_weibos(self, uid, max_pages=10, save_format='both'):
        """抓取指定用户的所有微博"""
        self.logger.info(f"开始抓取用户 {uid} 的微博数据...")
        
        # 获取用户信息
        user_info = self.get_user_info(uid)
        if not user_info:
            self.logger.error("无法获取用户信息，请检查UID是否正确")
            return None
        
        self.logger.info(f"用户信息: {user_info['screen_name']} - 粉丝数: {user_info['followers_count']}")
        
        # 获取微博列表
        weibos = self.get_user_weibo_list(uid, max_pages)
        
        if not weibos:
            self.logger.warning("没有获取到微博数据")
            return None
        
        self.logger.info(f"成功获取 {len(weibos)} 条微博")
        
        # 创建输出目录
        output_dir = f"weibo_data_{uid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存用户信息
        user_info_file = os.path.join(output_dir, 'user_info.json')
        with open(user_info_file, 'w', encoding='utf-8') as f:
            json.dump(user_info, f, ensure_ascii=False, indent=2)
        
        # 保存微博数据
        if save_format in ['csv', 'both']:
            csv_file = os.path.join(output_dir, 'weibos.csv')
            self.save_to_csv(weibos, csv_file)
        
        if save_format in ['json', 'both']:
            json_file = os.path.join(output_dir, 'weibos.json')
            self.save_to_json(weibos, json_file)
        
        return {
            'user_info': user_info,
            'weibos': weibos,
            'output_dir': output_dir
        }

def main():
    """主函数 - 示例用法"""
    scraper = WeiboScraper()
    
    # 示例：抓取某个用户的微博（需要替换为实际的UID）
    # UID可以通过访问用户主页的URL获取，例如：https://weibo.com/u/1234567890
    uid = input("请输入要抓取的微博用户UID: ").strip()
    
    if not uid:
        print("UID不能为空")
        return
    
    try:
        max_pages = int(input("请输入要抓取的页数（默认10页）: ").strip() or "10")
    except ValueError:
        max_pages = 10
    
    print(f"开始抓取用户 {uid} 的微博数据...")
    
    result = scraper.scrape_user_weibos(uid, max_pages=max_pages)
    
    if result:
        print(f"\n抓取完成！")
        print(f"用户: {result['user_info']['screen_name']}")
        print(f"获取微博数: {len(result['weibos'])}")
        print(f"数据保存在: {result['output_dir']}")
    else:
        print("抓取失败，请检查UID是否正确或网络连接")

if __name__ == "__main__":
    main()
