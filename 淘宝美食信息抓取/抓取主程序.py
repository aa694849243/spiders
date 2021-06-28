# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-19 0:03 
# ide： PyCharm
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from 淘宝美食信息抓取.config import *
import time
import re
from pyquery import PyQuery as pq
import pymongo
import pkgutil
options = webdriver.ChromeOptions()
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('start-fullscreen')
# 不加载图片,加快访问速度
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
browser = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(browser, 10)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def search():
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        time.sleep(1)
        submit.click()
        time.sleep(1)
        browser.find_element_by_css_selector('#fm-login-id').send_keys(USERNAME)
        time.sleep(1)
        browser.find_element_by_css_selector('#fm-login-password').send_keys(PASSWORD)
        time.sleep(1)
        browser.find_element_by_css_selector('#login-form > div.fm-btn > button').click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))).text
        get_product()
        return int(re.compile(r'(\d+)').search(total).groups(1)[0])
    except TimeoutException:
        return search()


def next_page(number):
    try:
        # print(f'{number=}')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(str(number))
        time.sleep(1)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(number)))
        get_product()

    except TimeoutException:
        next_page(number)


def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    i = 0
    for item in items:
        i += 1
        product = {
            'title': item.find('.title').text().strip(),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'shop': item.find('.shop').text()
        }
        if db[MONGO_TABLE].insert(product):
            print(f'插入数据库成功{i}')


def main():
    total = search()
    for i in range(2, total + 1):
        next_page(i)


if __name__ == '__main__':
    main()
