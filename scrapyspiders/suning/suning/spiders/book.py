# -*- coding: utf-8 -*-
from copy import deepcopy

import scrapy

from suning.items import SuningItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['http://book.suning.com/']

    def parse(self, response):
        doc = response.css('div.menu-list div.menu-item')
        for cls in doc:
            item = SuningItem()
            item['big_tag'] = doc.css('a::text').get()
            dd_as = cls.css('dd a')
            for smcls in dd_as:
                item['small_tag'] = smcls.css('::text').get()
                nexturl = smcls.css('::attr(href)').get()
                nexturl=nexturl.replace('https','http')
                yield scrapy.Request(url=nexturl, dont_filter=True, callback=self.parse_book_index,
                                     meta={'item': deepcopy(item), "is_selenium": True})

    def parse_book_index(self, response):
        item = response.meta['item']
        for product in response.css('li.product'):
            item['book_name'] = product.css(
                'div.res-info a.sellPoint::text').get().strip()
            item['book_price'] = ''.join(
                product.css('div.res-info em.prive.price::text').getall()).strip()
            item['book_shop'] = product.css(
                'div.res-info p.seller a::text').get().strip()
            yield item
        nexturl = 'http://list.suning.com' + \
            response.css('div.search-page a.next::attr(href)').get()
        if nexturl:
            yield scrapy.Request(nexturl, callback=self.parse_book_index, meta={'item': deepcopy(item), "is_selenium": True})
