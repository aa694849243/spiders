# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    big_tag = scrapy.Field()
    small_tag = scrapy.Field()
    # small_href = scrapy.Field()
    book_href = scrapy.Field()
    book_name = scrapy.Field()
    book_price = scrapy.Field()
    book_shop = scrapy.Field()
