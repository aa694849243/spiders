# -*- coding: utf-8 -*-

import scrapy

from quotes_t.items import QuotesTItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domain = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotesTItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
