#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博用户作品数据爬虫 - Selenium版本
支持处理更复杂的页面交互和反爬机制
"""

import time
import json
import pandas as pd
import logging
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WeiboSeleniumScraper:
    def __init__(self, headless=True):
        self.setup_logging()
        self.setup_driver(headless)
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('weibo_selenium_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self, headless=True):
        """设置Chrome驱动"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("Chrome驱动初始化成功")
        except Exception as e:
            self.logger.error(f"Chrome驱动初始化失败: {e}")
            raise
    
    def login_weibo(self, username=None, password=None):
        """登录微博（可选，某些内容需要登录才能查看）"""
        if not username or not password:
            self.logger.info("未提供登录信息，将以游客模式访问")
            return False
        
        try:
            self.driver.get('https://passport.weibo.cn/signin/login')
            time.sleep(3)
            
            # 输入用户名
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(username)
            
            # 输入密码
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            
            # 点击登录
            login_button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-login')]")
            login_button.click()
            
            # 等待登录完成
            time.sleep(5)
            
            if "passport.weibo.cn" not in self.driver.current_url:
                self.logger.info("登录成功")
                return True
            else:
                self.logger.warning("登录可能失败，继续以游客模式访问")
                return False
                
        except Exception as e:
            self.logger.error(f"登录失败: {e}")
            return False
    
    def get_user_profile(self, uid):
        """获取用户资料"""
        try:
            profile_url = f"https://m.weibo.cn/u/{uid}"
            self.driver.get(profile_url)
            time.sleep(3)
            
            # 获取用户基本信息
            user_info = {}
            
            try:
                # 用户名
                username_elem = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".m-text-cut"))
                )
                user_info['username'] = username_elem.text
            except:
                user_info['username'] = ''
            
            try:
                # 粉丝数、关注数、微博数
                stats_elems = self.driver.find_elements(By.CSS_SELECTOR, ".m-item-box .m-box-center .m-font-num")
                if len(stats_elems) >= 3:
                    user_info['weibo_count'] = stats_elems[0].text
                    user_info['following_count'] = stats_elems[1].text
                    user_info['followers_count'] = stats_elems[2].text
            except:
                user_info['weibo_count'] = '0'
                user_info['following_count'] = '0'
                user_info['followers_count'] = '0'
            
            try:
                # 简介
                desc_elem = self.driver.find_element(By.CSS_SELECTOR, ".m-text-box")
                user_info['description'] = desc_elem.text
            except:
                user_info['description'] = ''
            
            user_info['uid'] = uid
            user_info['profile_url'] = profile_url
            
            return user_info
            
        except Exception as e:
            self.logger.error(f"获取用户资料失败: {e}")
            return None
    
    def scroll_and_load_weibos(self, max_scrolls=10):
        """滚动页面加载更多微博"""
        scroll_count = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while scroll_count < max_scrolls:
            # 滚动到页面底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # 计算新的滚动高度
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                self.logger.info("已到达页面底部，没有更多内容")
                break
            
            last_height = new_height
            scroll_count += 1
            self.logger.info(f"已滚动 {scroll_count} 次")
    
    def extract_weibo_data(self):
        """提取页面上的微博数据"""
        weibos = []
        
        try:
            # 查找所有微博卡片
            weibo_cards = self.driver.find_elements(By.CSS_SELECTOR, ".m-item-box")
            
            for i, card in enumerate(weibo_cards):
                try:
                    weibo_data = {}
                    
                    # 微博文本内容
                    try:
                        text_elem = card.find_element(By.CSS_SELECTOR, ".m-text")
                        weibo_data['text'] = text_elem.text
                    except:
                        weibo_data['text'] = ''
                    
                    # 发布时间
                    try:
                        time_elem = card.find_element(By.CSS_SELECTOR, ".m-font-gray")
                        weibo_data['created_at'] = time_elem.text
                    except:
                        weibo_data['created_at'] = ''
                    
                    # 互动数据（点赞、评论、转发）
                    try:
                        action_elems = card.find_elements(By.CSS_SELECTOR, ".m-font-gray")
                        weibo_data['interactions'] = []
                        for elem in action_elems:
                            if elem.text and any(keyword in elem.text for keyword in ['赞', '评论', '转发']):
                                weibo_data['interactions'].append(elem.text)
                    except:
                        weibo_data['interactions'] = []
                    
                    # 图片链接
                    try:
                        img_elems = card.find_elements(By.CSS_SELECTOR, "img")
                        weibo_data['images'] = [img.get_attribute('src') for img in img_elems if img.get_attribute('src')]
                    except:
                        weibo_data['images'] = []
                    
                    # 微博链接
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, "a")
                        weibo_data['link'] = link_elem.get_attribute('href')
                    except:
                        weibo_data['link'] = ''
                    
                    weibo_data['index'] = i
                    weibos.append(weibo_data)
                    
                except Exception as e:
                    self.logger.error(f"提取第 {i} 条微博数据失败: {e}")
                    continue
            
            return weibos
            
        except Exception as e:
            self.logger.error(f"提取微博数据失败: {e}")
            return []
    
    def scrape_user_weibos(self, uid, max_scrolls=10, login_info=None):
        """抓取用户微博"""
        try:
            self.logger.info(f"开始抓取用户 {uid} 的微博...")
            
            # 登录（如果提供了登录信息）
            if login_info:
                self.login_weibo(login_info.get('username'), login_info.get('password'))
            
            # 获取用户资料
            user_info = self.get_user_profile(uid)
            if not user_info:
                self.logger.error("无法获取用户信息")
                return None
            
            self.logger.info(f"用户: {user_info['username']}")
            
            # 滚动加载微博
            self.scroll_and_load_weibos(max_scrolls)
            
            # 提取微博数据
            weibos = self.extract_weibo_data()
            
            self.logger.info(f"成功提取 {len(weibos)} 条微博")
            
            return {
                'user_info': user_info,
                'weibos': weibos
            }
            
        except Exception as e:
            self.logger.error(f"抓取失败: {e}")
            return None
    
    def save_data(self, data, output_dir=None):
        """保存数据"""
        if not output_dir:
            output_dir = f"weibo_selenium_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存用户信息
        user_info_file = os.path.join(output_dir, 'user_info.json')
        with open(user_info_file, 'w', encoding='utf-8') as f:
            json.dump(data['user_info'], f, ensure_ascii=False, indent=2)
        
        # 保存微博数据
        weibos_json_file = os.path.join(output_dir, 'weibos.json')
        with open(weibos_json_file, 'w', encoding='utf-8') as f:
            json.dump(data['weibos'], f, ensure_ascii=False, indent=2)
        
        # 保存为CSV
        try:
            df = pd.DataFrame(data['weibos'])
            csv_file = os.path.join(output_dir, 'weibos.csv')
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        except Exception as e:
            self.logger.error(f"保存CSV失败: {e}")
        
        self.logger.info(f"数据已保存到 {output_dir}")
        return output_dir
    
    def close(self):
        """关闭浏览器"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    """主函数"""
    scraper = None
    try:
        # 询问是否使用无头模式
        headless_input = input("是否使用无头模式？(y/n, 默认y): ").strip().lower()
        headless = headless_input != 'n'
        
        scraper = WeiboSeleniumScraper(headless=headless)
        
        # 获取用户输入
        uid = input("请输入要抓取的微博用户UID: ").strip()
        if not uid:
            print("UID不能为空")
            return
        
        try:
            max_scrolls = int(input("请输入滚动次数（默认10次）: ").strip() or "10")
        except ValueError:
            max_scrolls = 10
        
        # 询问是否需要登录
        need_login = input("是否需要登录？(y/n, 默认n): ").strip().lower() == 'y'
        login_info = None
        if need_login:
            username = input("请输入用户名: ").strip()
            password = input("请输入密码: ").strip()
            if username and password:
                login_info = {'username': username, 'password': password}
        
        # 开始抓取
        result = scraper.scrape_user_weibos(uid, max_scrolls, login_info)
        
        if result:
            # 保存数据
            output_dir = scraper.save_data(result)
            print(f"\n抓取完成！")
            print(f"用户: {result['user_info']['username']}")
            print(f"获取微博数: {len(result['weibos'])}")
            print(f"数据保存在: {output_dir}")
        else:
            print("抓取失败")
            
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
