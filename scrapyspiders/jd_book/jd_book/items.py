# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    b_cate = scrapy.Field()  # 图书所属一级分类名称
    s_cate = scrapy.Field()  # 图书所属二级分类名称
    # s_href = scrapy.Field()  # 图书所属二级分类地址
    book_name = scrapy.Field()  # 名称
    book_img = scrapy.Field()  # 封面图片地址
    book_author = scrapy.Field()  # 作者
    book_press = scrapy.Field()  # 出版社
    book_publish_date = scrapy.Field()  # 出版日期
    # book_sku = scrapy.Field()  # 商品编号
    book_price = scrapy.Field()  # 价格