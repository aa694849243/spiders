# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-17 0:51 
# ide： PyCharm
from hashlib import md5

import requests
import pymongo
from urllib.parse import urlencode
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from config import *
from multiprocessing import Pool
import os

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]

#标记一下
def get_page(page_num):
    args = {
        'keyword': KEY_WORD,
        'pd': 'atlas',
        'source': 'search_subtab_switch',
        'dvpf': 'pc',
        'aid': '4916',
        'page_num': page_num
    }
    url = 'https://so.toutiao.com/search?' + urlencode(args)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求页面出错')


def save_to_mongo(data):
    if db[MONGO_TABLE].insert(data):
        print('存储到db成功', data)
        return True
    return False


def parse_page(html):
    doc = pq(html)
    doc = doc('body div .s-result-list .result-content .col_R4Uluz')
    for col in doc.items():
        for div in col.children():
            yield {'url': pq(div)('img').attr('src'), 'title': pq(div)('[title]').attr('title')}


def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求页面出错')


def save_image(content):
    filepath = r'{0}\{1}.{2}'.format(r'F:\新建文件夹\爬虫相关\今日头条_天使猫猫\maomao', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(filepath):
        with open(filepath, 'wb') as f:
            f.write(content)
            f.close()


def get_image(html):
    for data in parse_page(html):
        if data:
            save_to_mongo(data)
            if 'url' in data:
                url = data['url']
                print(f'{url} 下载成功 ')
                download_image(data['url'])


def main(page_num):
    html = get_page(page_num)
    get_image(html)


if __name__ == '__main__':
    pool = Pool(5)
    pool.map(main, list(range(20)))
