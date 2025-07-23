#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本
检查Python版本和必要的依赖是否正确安装
"""

import sys
import platform
import subprocess
import importlib

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python版本过低，需要Python 3.7+")
        return False
    else:
        print("✅ Python版本符合要求")
        return True

def check_system_info():
    """检查系统信息"""
    system = platform.system()
    architecture = platform.architecture()[0]
    print(f"操作系统: {system} {platform.release()}")
    print(f"系统架构: {architecture}")
    
    return system

def check_required_packages():
    """检查必要的Python包"""
    required_packages = [
        'requests',
        'bs4',  # beautifulsoup4的导入名是bs4
        'pandas',
        'lxml',
        'fake_useragent'
    ]
    
    optional_packages = [
        'selenium',
        'webdriver_manager'
    ]
    
    print("\n检查必要的Python包:")
    all_required_installed = True
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            all_required_installed = False
    
    print("\n检查可选的Python包:")
    for package in optional_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"⚠️  {package} - 未安装（Selenium功能将不可用）")
    
    return all_required_installed

def check_network_connectivity():
    """检查网络连接"""
    print("\n检查网络连接:")
    try:
        import requests
        response = requests.get('https://httpbin.org/get', timeout=10)
        if response.status_code == 200:
            print("✅ 网络连接正常")
            return True
        else:
            print("❌ 网络连接异常")
            return False
    except Exception as e:
        print(f"❌ 网络连接测试失败: {e}")
        return False

def check_chrome_installation():
    """检查Chrome浏览器安装（用于Selenium）"""
    print("\n检查Chrome浏览器:")
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows路径
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in chrome_paths:
                try:
                    subprocess.run([path, '--version'], 
                                 capture_output=True, check=True, timeout=5)
                    print("✅ Chrome浏览器已安装")
                    return True
                except:
                    continue
        else:
            # Linux/macOS
            subprocess.run(['google-chrome', '--version'], 
                         capture_output=True, check=True, timeout=5)
            print("✅ Chrome浏览器已安装")
            return True
    except:
        pass
    
    print("⚠️  未检测到Chrome浏览器（Selenium功能将受限）")
    return False

def provide_installation_guide(system):
    """提供安装指南"""
    print(f"\n=== 安装指南 ({system}) ===")
    
    if system == "Windows":
        print("Windows用户请使用以下方法之一:")
        print("1. 运行 setup.ps1 (PowerShell脚本)")
        print("2. 运行 setup.bat (批处理脚本)")
        print("3. 查看 WINDOWS_GUIDE.md 获取详细指南")
    else:
        print("Linux/macOS用户请运行:")
        print("./setup.sh")
    
    print("\n手动安装命令:")
    print("pip install -r requirements.txt")

def main():
    """主函数"""
    print("=== 微博爬虫环境检查 ===\n")
    
    # 检查Python版本
    python_ok = check_python_version()
    
    # 检查系统信息
    system = check_system_info()
    
    # 检查包安装
    packages_ok = check_required_packages()
    
    # 检查网络连接
    network_ok = check_network_connectivity()
    
    # 检查Chrome安装
    chrome_ok = check_chrome_installation()
    
    # 总结
    print(f"\n=== 检查结果 ===")
    print(f"Python版本: {'✅' if python_ok else '❌'}")
    print(f"必要包安装: {'✅' if packages_ok else '❌'}")
    print(f"网络连接: {'✅' if network_ok else '❌'}")
    print(f"Chrome浏览器: {'✅' if chrome_ok else '⚠️'}")
    
    if python_ok and packages_ok and network_ok:
        print("\n🎉 环境检查通过！可以开始使用微博爬虫了。")
        print("运行 'python quick_start.py' 查看使用示例")
    else:
        print("\n❌ 环境检查未通过，请先解决上述问题。")
        provide_installation_guide(system)

if __name__ == "__main__":
    main()
