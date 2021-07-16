# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class JdBookPipeline:
    def __init__(self):
        conn = MongoClient('localhost')
        # 创建数据库以及要保存到的集合
        self.home = conn["jd"]["book"]
    def process_item(self, item, spider):
        try:
            self.home.insert(dict(item))
        except:
            print('wrong')
        return item
