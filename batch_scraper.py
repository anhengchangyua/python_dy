#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量抓取多个微博用户数据的脚本
"""

import json
import time
import os
from datetime import datetime
from weibo_scraper import WeiboScraper

class BatchWeiboScraper:
    def __init__(self):
        self.scraper = WeiboScraper()
        
    def load_user_list(self, file_path):
        """从文件加载用户列表"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.json'):
                    return json.load(f)
                else:
                    # 假设是文本文件，每行一个UID
                    return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"加载用户列表失败: {e}")
            return []
    
    def scrape_multiple_users(self, user_list, max_pages=5, delay=10):
        """批量抓取多个用户"""
        results = {}
        total_users = len(user_list)
        
        for i, uid in enumerate(user_list, 1):
            print(f"\n正在处理第 {i}/{total_users} 个用户: {uid}")
            
            try:
                result = self.scraper.scrape_user_weibos(uid, max_pages=max_pages)
                
                if result:
                    results[uid] = {
                        'success': True,
                        'user_info': result['user_info'],
                        'weibo_count': len(result['weibos']),
                        'output_dir': result['output_dir'],
                        'scrape_time': datetime.now().isoformat()
                    }
                    print(f"✅ 成功抓取用户 {result['user_info']['screen_name']}")
                else:
                    results[uid] = {
                        'success': False,
                        'error': 'Failed to scrape',
                        'scrape_time': datetime.now().isoformat()
                    }
                    print(f"❌ 抓取用户 {uid} 失败")
                
            except Exception as e:
                results[uid] = {
                    'success': False,
                    'error': str(e),
                    'scrape_time': datetime.now().isoformat()
                }
                print(f"❌ 抓取用户 {uid} 出现异常: {e}")
            
            # 添加延时避免被封
            if i < total_users:
                print(f"等待 {delay} 秒后继续...")
                time.sleep(delay)
        
        return results
    
    def save_batch_results(self, results):
        """保存批量抓取结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f'batch_results_{timestamp}.json'
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 生成统计报告
        total_users = len(results)
        success_count = sum(1 for r in results.values() if r['success'])
        fail_count = total_users - success_count
        
        report = f"""
批量抓取完成报告
================
抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
总用户数: {total_users}
成功数量: {success_count}
失败数量: {fail_count}
成功率: {success_count/total_users*100:.1f}%

详细结果已保存到: {results_file}
"""
        
        print(report)
        
        # 保存报告
        report_file = f'batch_report_{timestamp}.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
            f.write("\n\n详细结果:\n")
            for uid, result in results.items():
                if result['success']:
                    f.write(f"✅ {uid}: {result['user_info']['screen_name']} - {result['weibo_count']} 条微博\n")
                else:
                    f.write(f"❌ {uid}: {result['error']}\n")
        
        return results_file, report_file

def main():
    """主函数"""
    print("=== 微博批量抓取工具 ===")
    
    # 获取用户输入
    print("请选择用户列表输入方式:")
    print("1. 从文件读取")
    print("2. 手动输入")
    
    choice = input("请选择 (1/2): ").strip()
    
    user_list = []
    
    if choice == '1':
        file_path = input("请输入用户列表文件路径: ").strip()
        if os.path.exists(file_path):
            batch_scraper = BatchWeiboScraper()
            user_list = batch_scraper.load_user_list(file_path)
        else:
            print("文件不存在")
            return
    
    elif choice == '2':
        print("请输入用户UID列表，每行一个，输入空行结束:")
        while True:
            uid = input().strip()
            if not uid:
                break
            user_list.append(uid)
    
    else:
        print("无效选择")
        return
    
    if not user_list:
        print("用户列表为空")
        return
    
    print(f"共 {len(user_list)} 个用户待抓取")
    
    # 获取抓取参数
    try:
        max_pages = int(input("每个用户抓取页数 (默认5): ").strip() or "5")
        delay = int(input("用户间延时秒数 (默认10): ").strip() or "10")
    except ValueError:
        max_pages = 5
        delay = 10
    
    # 开始批量抓取
    batch_scraper = BatchWeiboScraper()
    results = batch_scraper.scrape_multiple_users(user_list, max_pages, delay)
    
    # 保存结果
    batch_scraper.save_batch_results(results)

if __name__ == "__main__":
    main()
