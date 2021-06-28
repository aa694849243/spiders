# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-24 3:05 
# ide： PyCharm
from selenium import webdriver
import time
import json
from selenium import webdriver
import json

# 填写webdriver的保存目录
driver = webdriver.Chrome()

# 记得写完整的url 包括http和https
driver.get('https://weixin.sogou.com')
# driver.refresh()
# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()

with open(r'F:\新建文件夹\爬虫相关\搜狗微信文章\cookies.txt','r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)

    # 方法1 将expiry类型变为int
    # for cookie in cookies_list:
    #     # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
    #     if isinstance(cookie.get('expiry'), float):
    #         cookie['expiry'] = int(cookie['expiry'])
    #     driver.add_cookie(cookie)

    # 方法2删除该字段
    for cookie in cookies_list:
        print(cookie)
        # 该字段有问题所以删除就可以
        # if 'expiry' in cookie:
        #     del cookie['expiry']
        # driver.add_cookie(cookie)
driver.refresh()
driver.get('https://weixin.sogou.com/weixin?type=2&query=%E9%A3%8E%E6%99%AF')
# driver.close()'
# driver.get('https://weixin.sogou.com/')