# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-23 1:53
# ide： PyCharm
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from 搜狗微信文章.config import *
import time
import re
from pyquery import PyQuery as pq
import pymongo
from selenium import webdriver
import time
import json

# 填写webdriver的保存目录
driver = webdriver.Chrome()

# 记得写完整的url 包括http和https
driver.get('https://weixin.sogou.com')

# 程序打开网页后20秒内 “手动登陆账户”
time.sleep(20)

with open('cookies.txt', 'w') as f:
    # 将cookies保存为json格式
    f.write(json.dumps(driver.get_cookies()))

driver.close()
