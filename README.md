# 微博用户作品数据爬虫

这是一个功能完整的微博用户作品数据爬虫项目，支持抓取指定用户的所有微博内容、互动数据等信息。

## 功能特性

- ✅ 抓取用户基本信息（用户名、粉丝数、关注数等）
- ✅ 抓取用户所有微博内容
- ✅ 获取微博互动数据（点赞、评论、转发数）
- ✅ 下载微博图片链接
- ✅ 支持视频链接获取
- ✅ 处理转发微博
- ✅ 多种输出格式（JSON、CSV）
- ✅ 反爬虫机制规避
- ✅ 两种爬虫模式（API模式和Selenium模式）

## 项目结构

```
weibo-scraper/
├── weibo_scraper.py          # 基于API的爬虫（推荐）
├── weibo_selenium_scraper.py # 基于Selenium的爬虫
├── get_uid.py               # UID获取工具
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
└── README.md               # 使用说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 获取用户UID

首先需要获取要抓取的微博用户的UID：

```bash
python get_uid.py
```

支持两种方式：
- 从微博链接提取UID
- 通过用户名关键词搜索

### 2. 基础爬虫（推荐）

使用基于API的爬虫，速度快，稳定性好：

```bash
python weibo_scraper.py
```

运行后按提示输入：
- 用户UID
- 要抓取的页数

### 3. 高级爬虫

使用基于Selenium的爬虫，可以处理更复杂的情况：

```bash
python weibo_selenium_scraper.py
```

支持的功能：
- 无头/有头模式选择
- 可选择是否登录
- 自动滚动加载更多内容

## 输出数据格式

### 用户信息 (user_info.json)
```json
{
  "uid": "1234567890",
  "screen_name": "用户名",
  "followers_count": 1000000,
  "follow_count": 500,
  "statuses_count": 2000,
  "description": "用户简介",
  "verified": true,
  "verified_reason": "认证信息"
}
```

### 微博数据 (weibos.json/weibos.csv)
```json
[
  {
    "id": "微博ID",
    "created_at": "发布时间",
    "text": "微博文本内容",
    "text_raw": "原始文本",
    "source": "发布来源",
    "reposts_count": 转发数,
    "comments_count": 评论数,
    "attitudes_count": 点赞数,
    "pics": ["图片链接列表"],
    "video_url": "视频链接",
    "retweeted_status": "转发微博信息",
    "user_id": "用户ID",
    "user_name": "用户名"
  }
]
```

## 配置说明

可以通过修改 `config.py` 来调整爬虫参数：

- `REQUEST_CONFIG`: 请求配置（超时时间、重试次数等）
- `USER_AGENTS`: 用户代理列表
- `WEIBO_CONFIG`: 微博API配置
- `OUTPUT_CONFIG`: 输出格式配置
- `SELENIUM_CONFIG`: Selenium配置

## 注意事项

### 1. 合规使用
- 请遵守微博的使用条款和robots.txt
- 不要过于频繁地请求，避免对服务器造成压力
- 仅用于学习和研究目的

### 2. 反爬虫应对
- 程序已内置请求间隔和随机User-Agent
- 如遇到验证码或IP封禁，请降低抓取频率
- 可以考虑使用代理IP（需自行配置）

### 3. 数据完整性
- 某些微博可能因为隐私设置而无法获取
- 删除的微博无法抓取
- 部分数据可能需要登录才能访问

## 常见问题

### Q: 如何获取用户UID？
A: 使用 `get_uid.py` 工具，支持从链接提取或搜索用户名。

### Q: 抓取失败怎么办？
A: 检查网络连接，确认UID正确，降低抓取频率。

### Q: 需要登录吗？
A: 大部分公开内容无需登录，但某些内容可能需要登录访问。

### Q: 如何处理大量数据？
A: 程序支持分页抓取，可以分批次进行，避免一次性抓取过多数据。

## 法律声明

本项目仅供学习和研究使用，使用者需要遵守相关法律法规和网站服务条款。作者不承担因使用本项目而产生的任何法律责任。

## 更新日志

- v1.0.0: 基础功能实现
- v1.1.0: 添加Selenium支持
- v1.2.0: 优化反爬虫机制
- v1.3.0: 添加UID获取工具

## 技术支持

如有问题，请提交Issue或联系作者。

---

**免责声明**: 请合理使用本工具，遵守相关法律法规和网站条款。
