---
title: Python网络爬虫入门
created: 2022-09-17 16:24:37
updated: 2022-09-17 17:13:38
tags: 
- article
---
# Python网络爬虫入门

## 爬虫简介

### 合法性

- 抓取数据时现实生活中真实数据则合法
- 抓取数据为原创数据则受版权保护

### 背景调研

#### 检查 robots.txt

- 检查 robots.txt 可以最小化爬虫被封禁的可能
- 发现和网络结构相关的线索

##### 查看方法

通过访问 http://example.webscraping.com/**robots.txt**, 得到内容:  

```http
## section 1
User-agent: BadCrawler  // 禁止用户代理为 BadCrawler 的爬虫爬取网站
Disallow: /

## section 2
User-agent: *
Disallow: /trap       // 封禁爬取不允许链接的爬虫
Crawl-delay: 5        // 两次请求应间隔 5 秒

## section 3
Sitemap: http://example.webscraping.com/sitemap.xml
```

#### 检查网站地图

- Sitemap 文件帮助爬虫定位最新的文件, 而无需爬取每一个网页
- 网站地图提供了所以网页的链接
- 该文件经常存在缺失, 过期或不完整的问题

##### 查看方法

通过访问 robots.txt 中定义的地图链接地址 http://example.webscraping.com/sitemap.xml

```sh
http://example.webscraping.com/places/default/view/Afghanistan-1
http://example.webscraping.com/places/default/view/Aland-Islands-2
http://example.webscraping.com/places/default/view/Albania-3
http://example.webscraping.com/places/default/view/Algeria-4
http://example.webscraping.com/places/default/view/American-Samoa-5
http://example.webscraping.com/places/default/view/Andorra-6
http://example.webscraping.com/places/default/view/Angola-7
http://example.webscraping.com/places/default/view/Anguilla-8
http://example.webscraping.com/places/default/view/Antarctica-9
http://example.webscraping.com/places/default/view/Antigua-and-Barbuda-10
......
```

#### 估算网站大小

- 目标网站的大小会影响我们如何进行爬取

##### 估算方法

- 一个简单的方法是检查 Google 爬虫的结果, Google 很可能已经爬取过我们感兴趣的网站
- 通过搜索的 `site` 关键词过滤域名结
    - 在域名后添加 url 可以对结果进行过滤, 仅显示网页某些部分
    - 可以从 http://www.google.com/advanced_search 了解参数

```
site:example.webscraping.com       // 搜索全站
site:example.webscraping.com/places/default/view  // 只搜索国家页面
```

#### 识别网站所用技术

使用 builtwith 模块检查网站构建的技术类型:

```sh
pip install builtwish
```

用法:

```python
>>> import builtwith
>>> builtwith.parse('http://example.webscraping.com')

{u'javascript-frameworks': [u'jQuery', u'Modernizr', u'jQuery UI'], u'web-frameworks': [u'Web2py', u'Twitter Bootstrap'], u'programming-languages': [u'Python'], u'web-servers': [u'Nginx']}
``` 

通过返回的信息, 该网站使用 python 的 web2py 框架, 还使用了一些 JavaScript 库, 因此内容可能嵌入在 HTML 中.

#### 寻找网站所有者

根据所有者来调整爬虫策略.

##### WHOIS 查询

```sh
pip install python-whois
```

用法:

```python
>>> import whois
>>> print whois.whois('webscraping.com')

{
  "updated_date": [
    "2013-08-20 08:08:30", 
    "2013-08-20 08:08:29"
  ], 
  "status": [
    "clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited", 
    "clientRenewProhibited https://icann.org/epp#clientRenewProhibited", 
    "clientTransferProhibited https://icann.org/epp#clientTransferProhibited", 
    "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited", 
    "clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited", 
    "clientUpdateProhibited http://www.icann.org/epp#clientUpdateProhibited", 
    "clientRenewProhibited http://www.icann.org/epp#clientRenewProhibited", 
    "clientDeleteProhibited http://www.icann.org/epp#clientDeleteProhibited"
  ], 
  "name": null, 
  "dnssec": "unsigned", 
  "city": null, 
  "expiration_date": "2020-06-26 18:01:19", 
  "zipcode": null, 
  "domain_name": "WEBSCRAPING.COM", 
  "country": "AU", 
  "whois_server": "whois.godaddy.com", 
  "state": "Victoria", 
  "registrar": "GoDaddy.com, LLC", 
  "referral_url": null, 
  "address": null, 
  "name_servers": [
    "NS1.WEBFACTION.COM", 
    "NS2.WEBFACTION.COM", 
    "NS3.WEBFACTION.COM", 
    "NS4.WEBFACTION.COM"
  ], 
  "org": null, 
  "creation_date": "2004-06-26 18:01:19", 
  "emails": "abuse@godaddy.com"
}

```

### 编写第一个爬虫

爬取 (srawling) 一般方式:
- 爬取网站地图
- 遍历每个网页的数据库 ID
- 跟踪网页链接

#### 下载网页

使用 urllib2 模块下载 URL:  

download.py:

```python
## coding=utf-8
import urllib2


def download(url, num_retries = 2):
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
    if num_retries > 0:
        if hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, num_retries - 1)
    return html
```

test.py:

```python
## coding=utf-8
import download

url = raw_input("please type the url:")  ## 输入url
html = download.download(url)
print html
```

## 实际项目

### 插件

- requests
    - 爬取网页
- bs4
    - 解析爬取的内容
- openpyxl
    - 导出 excel

### user-agent

浏览器中 F12, 网络一栏找到加载的一个 html文件. 里面有 user-agent 字段.  

```python
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
```