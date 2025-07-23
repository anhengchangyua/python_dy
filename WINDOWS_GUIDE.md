# Windows 用户使用指南

本指南专门为Windows用户提供详细的安装和使用说明。

## 系统要求

- Windows 10/11 或 Windows Server 2016+
- Python 3.7+ (推荐Python 3.9+)
- 至少2GB可用磁盘空间

## 安装步骤

### 方法一：使用PowerShell脚本（推荐）

1. **以管理员身份运行PowerShell**
   - 按 `Win + X`，选择"Windows PowerShell (管理员)"
   - 或搜索"PowerShell"，右键选择"以管理员身份运行"

2. **设置执行策略（如果需要）**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **运行安装脚本**
   ```powershell
   .\setup.ps1
   ```

### 方法二：使用批处理脚本

1. **双击运行 `setup.bat`**
   - 或在命令提示符中运行：`setup.bat`

### 方法三：手动安装

1. **检查Python安装**
   ```cmd
   python --version
   ```
   如果未安装，请从 https://www.python.org/downloads/ 下载安装

2. **创建虚拟环境**
   ```cmd
   python -m venv venv
   ```

3. **激活虚拟环境**
   ```cmd
   venv\Scripts\activate.bat
   ```

4. **安装依赖**
   ```cmd
   pip install -r requirements.txt
   ```

## 使用方法

### 1. 激活虚拟环境

每次使用前都需要激活虚拟环境：

**命令提示符 (CMD):**
```cmd
venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

### 2. 运行程序

```cmd
# 快速入门
python quick_start.py

# 获取用户UID
python get_uid.py

# 基础爬虫
python weibo_scraper.py

# Selenium爬虫
python weibo_selenium_scraper.py

# 批量抓取
python batch_scraper.py
```

## 常见问题

### Q1: PowerShell提示"无法加载文件，因为在此系统上禁止运行脚本"

**解决方案：**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q2: 提示"python不是内部或外部命令"

**解决方案：**
1. 确保已安装Python
2. 检查Python是否添加到PATH环境变量
3. 尝试使用 `py` 命令代替 `python`

### Q3: pip安装依赖失败

**解决方案：**
```cmd
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Q4: Selenium相关错误

**解决方案：**
1. 确保已安装Chrome浏览器
2. 程序会自动下载ChromeDriver
3. 如果仍有问题，尝试手动下载ChromeDriver并放到PATH中

### Q5: 中文编码问题

**解决方案：**
在命令提示符中运行：
```cmd
chcp 65001
```

## Chrome浏览器设置

如果使用Selenium爬虫，建议：

1. **安装Chrome浏览器**
   - 下载地址：https://www.google.com/chrome/

2. **允许自动下载ChromeDriver**
   - 程序会自动处理，无需手动操作

## 防火墙设置

如果遇到网络问题：

1. **允许Python通过防火墙**
   - Windows安全中心 → 防火墙和网络保护 → 允许应用通过防火墙

2. **检查代理设置**
   - 如果使用代理，可能需要配置pip代理

## 性能优化

1. **关闭不必要的程序**
   - 爬虫运行时关闭其他占用内存的程序

2. **调整爬虫参数**
   - 在 `config.py` 中调整请求间隔和并发数

3. **使用SSD硬盘**
   - 数据保存到SSD可以提高IO性能

## 数据存储

爬取的数据默认保存在：
- `weibo_data_[UID]_[时间戳]/` 目录下
- 包含JSON和CSV格式文件

## 卸载

如需卸载项目：

1. **删除虚拟环境**
   ```cmd
   rmdir /s venv
   ```

2. **删除项目文件夹**
   - 直接删除整个项目目录即可

## 技术支持

如遇到问题：
1. 查看 `README.md` 主要文档
2. 检查日志文件 `weibo_scraper.log`
3. 确保网络连接正常
4. 尝试降低抓取频率

---

**注意事项：**
- 请遵守微博使用条款
- 仅用于学习和研究目的
- 注意保护用户隐私
- 避免过度频繁的请求
