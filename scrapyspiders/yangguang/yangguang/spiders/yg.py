# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import scrapy

from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest']

    def parse(self, response):
        self.logger.info('开始爬取数据')
        items = response.css('li.clear')
        for i in items:
            item = YangguangItem()
            item['number'] = i.css('span:nth-child(1)::text').get()
            item['status'] = i.css('span:nth-child(2)::text').get().strip()
            item['title'] = i.css('span:nth-child(3) a::text').get().strip()
            detail_url = response.urljoin(i.css('span:nth-child(3) a::attr(href)').get())
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
        # next = response.css('a.arrow-page.prov_rota::attr(href)').get()
        for next in range(2, 20):
            index = {'id': 1, 'page': next}
            newurl = 'https://wz.sun0769.com/political/index/politicsNewest?'+urlencode(index)
            if newurl is not None:
                yield scrapy.Request(newurl, callback=self.parse)

    def parse_detail(self, response):
        self.logger.info('分析详情页')
        item = response.meta['item']
        item['content'] = response.css('div.details-box pre::text').get().strip()
        item['publish_date'] = response.css('div.focus-date.clear span:nth-child(2)::text').get().strip()
        print(item)
        yield item
