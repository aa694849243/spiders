# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-24 14:55 
# ide： PyCharm
from urllib.parse import urlencode

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from 搜狗微信文章.config import *
from requests.exceptions import ConnectionError
import time
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
import pymongo
import json

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
headers = {
    'Cookie': 'ssuid=5108455100; SUID=6031113A2613910A000000005FD3904C; SUV=1621620936829305; ABTEST=0|1621620940|v1; weixinIndexVisited=1; ssppuid=SXVcgy/BP8XoaM4HrMUyYSSKsyCJy88IFuSG5LFrtdmaTa3bA4OJu0CvHl+9SSdY; ssppunid=67ZLsYqA+fElD35S2YRIdw==; JSESSIONID=aaaogZBXIg8G282txAHGx; IPLOC=CN; SNUID=4E6C55E1C5C005D2442B5C8EC642521E; ppinf=5|1621883258|1623092858|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4MzpBMCVFNSVCMSU4QiVFNyVCRSU4RSVFNyU4OSVCOSVFNyU4RSVBRiVFNCVCRiU5RCVFNyU5NCVCMiVFOSU4NiU5QiVFNiVBMyU4MCVFNiVCNSU4QnxjcnQ6MTA6MTYyMTg4MzI1OHxyZWZuaWNrOjgzOkEwJUU1JUIxJThCJUU3JUJFJThFJUU3JTg5JUI5JUU3JThFJUFGJUU0JUJGJTlEJUU3JTk0JUIyJUU5JTg2JTlCJUU2JUEzJTgwJUU2JUI1JThCfHVzZXJpZDo0NDpvOXQybHVMSGJtMW5kTzNNU3p0aWtiZmFYMWo4QHdlaXhpbi5zb2h1LmNvbXw; pprdig=ctWVO-fOnJ2Mck0WOf9gpl4Ubs08tkAJtzfjJ_WuukZa_rembuy_KONkWmmFuFAyXPhKfr9RGBorEndvqHyPyExCeh6IdeJ1mLQXNhKIX6Cx029Eh62v3-1Ez0zdEc21sIZQ-ODxEHxoTR3uVxwY8uX2iUQEwEJDkwRnV-m1kR8; ppinfo=8e4134a002; passport=5|1621883258|1623092858|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4MzpBMCVFNSVCMSU4QiVFNyVCRSU4RSVFNyU4OSVCOSVFNyU4RSVBRiVFNCVCRiU5RCVFNyU5NCVCMiVFOSU4NiU5QiVFNiVBMyU4MCVFNiVCNSU4QnxjcnQ6MTA6MTYyMTg4MzI1OHxyZWZuaWNrOjgzOkEwJUU1JUIxJThCJUU3JUJFJThFJUU3JTg5JUI5JUU3JThFJUFGJUU0JUJGJTlEJUU3JTk0JUIyJUU5JTg2JTlCJUU2JUEzJTgwJUU2JUI1JThCfHVzZXJpZDo0NDpvOXQybHVMSGJtMW5kTzNNU3p0aWtiZmFYMWo4QHdlaXhpbi5zb2h1LmNvbXw|84fccda1d0|ctWVO-fOnJ2Mck0WOf9gpl4Ubs08tkAJtzfjJ_WuukZa_rembuy_KONkWmmFuFAyXPhKfr9RGBorEndvqHyPyExCeh6IdeJ1mLQXNhKIX6Cx029Eh62v3-1Ez0zdEc21sIZQ-ODxEHxoTR3uVxwY8uX2iUQEwEJDkwRnV-m1kR8; sgid=30-52631759-AWCribXpRcuGIGdVV6LgtkTs; ppmdig=16218832580000008c3288c1ff48c95bdc9bb236b50426a0',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


ip = get_proxy()


def get_html(url, count):
    print('Crawling', url)
    print('Trying Count', count)
    global ip
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if ip:
            proxies = {
                'http': 'http://' + ip,
                'https': 'https://' + ip
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            ip = get_proxy()
            if ip:
                print('Using Proxy', ip)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        ip = get_proxy()
        count += 1
        return get_html(url, count)


def get_url():
    with open('article_url.txt', 'r') as f:
        while line := f.readline():
            yield line


def save_to_mogodb(html):
    doc = pq(html)
    article={}
    article['title']=doc('#activity-name').text().strip()
    article['author']=doc('#js_name').text().strip()
    article['content']=doc('#js_content').text().strip()
    if db['articles'].update({'title': article['title']}, {'$set': article}, True):
        print('Saved to Mongo', article['title'])
    else:
        print('Saved to Mongo Failed', article['title'])

def main():
    for url in get_url():
        html = get_html(url,0)
        save_to_mogodb(html)

if __name__ == '__main__':
    main()
