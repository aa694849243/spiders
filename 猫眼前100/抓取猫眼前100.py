# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-05-14 0:11 
# ide： PyCharm
import time

import requests, json, lxml, re
from lxml import etree
from selenium import webdriver
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import json
from multiprocessing import Pool


def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None
    except:
        return None


def parse_page(html):
    pattern = re.compile(
        r'class="rank-number".*?>(.*?)<.*?img" src="(.*?)".*?class="title".*?>(.*?)<.*?class="actors".*?>(.*?)<.*?class="number".*?>(.*?)<',
        re.S)  # alt="(.*?)".*?"actors".*?>(.*?)</div>.*?"number".*?>(.*?)</span>
    items = re.findall(pattern, html)

    doc = pq(html)
    a = doc("#app > div > div.board-movie")
    items = a('.board-card').items()
    for item in items:
        yield {
            'number': item.find('.rank-number').text(),
            'title': item.find('.title').text(),
            'actors': item.find('.actors').text(),
            'score': item.find('.number').text(),
            'image': item.find('.img').attr('src')
        }


def main():
    url = r'https://m.maoyan.com/board/4'
    html = get_page(url)
    for item in parse_page(html):
        with open('猫眼前100.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print(end - start)
