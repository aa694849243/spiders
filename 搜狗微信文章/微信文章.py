# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-23 1:53 
# ide： PyCharm
from urllib.parse import urlencode

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from 搜狗微信文章.config import *
import time
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
import pymongo
import json


# "origin": "39.144.170.189"

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


base_url = 'http://weixin.sogou.com/weixin?'
options = webdriver.ChromeOptions()
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')
options.add_argument('disable-gpu')
# options.add_argument('start-fullscreen')
# 不加载图片,加快访问速度
# options.add_argument('--proxy-server=%s' % ip)
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
options.add_argument(
    'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
browser = webdriver.Chrome(options=options)
# a=browser.get('https://httpbin.org/ip')
wait = WebDriverWait(browser, 10)
# t = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > pre'))).text
# print(t)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
prefix = 'https://weixin.sogou.com'


def get_cookies(url, browser):
    browser.get(url)
    # driver.refresh()
    # 首先清除由于浏览器打开已有的cookies
    browser.delete_all_cookies()

    with open(r'F:\新建文件夹\爬虫相关\搜狗微信文章\cookies.txt', 'r') as f:
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
            # 该字段有问题所以删除就可以
            if 'expiry' in cookie:
                del cookie['expiry']
            browser.add_cookie(cookie)
    browser.refresh()


get_cookies(prefix, browser)


def search(url, browser, count):
    if count > MAX_COUNT:
        print('这个网页打不开')
        return
    try:
        browser.get(url)
        for postfix in get_article_url():
            if postfix.startswith(prefix):
                article_url = prefix
            else:
                article_url = prefix + postfix
            time.sleep(1)
            with open('article_url.txt', 'a') as f:
                f.write(article_url + '\n')
            try:
                get_article_detail(article_url)
            finally:
                continue


    except TimeoutException:
        print('更换ip')
        ip = get_proxy()
        options.add_argument('--proxy-server=%s' % ip)
        browser = webdriver.Chrome(options=options)
        return search(url, browser, count + 1)


def get_article_url():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main > div.news-box > ul')))
    html = browser.page_source
    doc = pq(html)
    doc = doc('#main > div.news-box > ul')
    for item in doc('li').items():
        yield item('[href]').attr('href')


def get_article_detail(url):
    browser.get(url)
    html = browser.page_source
    doc = pq(html)
    article = dict()
    article['title'] = doc('#activity-name').text().strip()
    article['author'] = doc('#meta_content > span.rich_media_meta.rich_media_meta_text').text().strip()
    article['content'] = doc('#js_content').text()
    print(article)
    with open('article_content','a') as f:
        f.write(json.dumps(article))
    save_to_mongodb(article)


def save_to_mongodb(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = search(url, browser, 0)
    return html


def main():
    for page in range(1, 20):
        get_index(KEY_WORD, page)
        time.sleep(1)


if __name__ == '__main__':
    main()
