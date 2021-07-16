# -*- coding: utf-8 -*-
import json
from copy import deepcopy

import scrapy

from jd_book.items import JdBookItem


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com']
    start_urls = ['https://pjapi.jd.com/book/sort?source=bookSort&callback=jsonp_1624856707553_24193']

    def parse(self, response):
        t = response.text
        l = t.index('{')
        t = t[l:-1]
        a = json.loads(t)['data']
        for b in a:
            item = JdBookItem()
            item['b_cate'] = b['categoryName']
            url_id = [str(int(b['fatherCategoryId'])), str(int(b['categoryId']))]
            for c in b['sonList']:
                item['s_cate'] = c['categoryName']
                if len(url_id) == 2:
                    url_id.append(str(int(c['categoryId'])))
                else:
                    url_id[-1] = str(int(c['categoryId']))
                num = ','.join(url_id)
                url = 'http://list.jd.com/list.html?cat={}'.format(num)
                yield scrapy.Request(url, callback=self.parse_books, meta={'item': deepcopy(item), 'number': 1})

    def parse_books(self, response):
        item = response.meta['item']
        number = response.meta['number']
        for li in response.css('ul.gl-warp li.gl-item'):
            item['book_name'] = li.css('div.p-name a em::text').get().strip()
            item['book_img'] = li.css('div.p-img img::attr(data-lazy-img)').get()
            if not item['book_img']:
                item['book_img'] = li.css('div.p-img img::attr(src)').get()
            item['book_img'] = 'https://' + item["book_img"]
            item['book_author'] = li.css('div.p-bookdetails span.p-bi-name a::text').get()
            item["book_press"] = li.css('div.p-bookdetails span.p-bi-store a::text').get()
            item["book_publish_date"] = li.css('div.p-bookdetails span.p-bi-date::text').get()
            item["book_price"] = li.css('div.p-price strong i::text').get()
            yield item
        if number < 200:
            url = response.url
            if 'page' in url:
                index = url.index('page')
                nexturl = url[:index] + 'page=' + str(number)
            else:
                nexturl = url + '&page=' + str(number)
            if 'https' in nexturl:
                nexturl = nexturl.replace('https', 'http')
            yield scrapy.Request(nexturl, callback=self.parse_books, meta={'item': deepcopy(item), 'number': number+1})
