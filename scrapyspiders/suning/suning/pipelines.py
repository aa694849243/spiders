# -*- coding: utf-8 -*-

from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chorme_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

class SuningPipeline:
    def __init__(self):
        """定义MongoDB对象，保存数据"""
        # 创建连接对象
        conn = MongoClient('localhost')
        # 创建数据库以及要保存到的集合
        self.home = conn["suning"]["book"]

    def open_spider(self, spider):
        """开启爬虫"""
        # 创建一个selenium的chrome浏览器对象
        # spider.driver = webdriver.Chrome(chrome_options=chrome_options)
        pass
    def process_item(self, item, spider):
        try:
            self.home.insert(dict(item))
        except:
            print('wrong')
        return item

    def close_spider(self, spider):
        """爬虫处理完数据关闭爬虫"""
        spider.driver.quit()
