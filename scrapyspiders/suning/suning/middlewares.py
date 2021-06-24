# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver


class SuningSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SuningDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.http import TextResponse
import time
import requests


def get_proxy():
    try:
        response = requests.get('http://127.0.0.1:5555/random')
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


class SeleniumMid(object):
    def process_request(self, request, spider):
        # 使用在管道中开启爬虫open_spider方法中定义的selenium对象请求url
        # 做到集成爬取数据
        # 因为每次请求都会去请求robots协议，这里判断如果是请求robots，不在selenium中做
        if spider.name == "book" and request.meta.get("is_selenium"):
            options = webdriver.ChromeOptions()
            options.add_argument('disable-gpu')
            options.add_argument('--headless')
            # while True:
            #     ip = get_proxy()
            #     headers = {
            #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
            #     }
            #     proxies = {'http': 'http://' + ip}
            #     try:
            #         r = requests.get(request.url, headers=headers, proxies=proxies)
            #         if r.status_code == 200:
            #             break
            #     except:
            #         continue
            # 
            # options.add_argument('--proxy-server=%s' % ip)
            browser = webdriver.Chrome(chrome_options=options)
            browser.get(request.url)
            # selenium调用js的方法，里面传入的是执行的js代码
            browser.execute_script("window.scrollTo(0,10000)")
            time.sleep(3)

            browser.execute_script("window.scrollTo(0,10000)")
            time.sleep(3)
            # 这里得到的内容是element中的内容，包含js和css请求后的所有内容
            content = browser.page_source

            response = TextResponse(url=browser.current_url, body=content.encode(), request=request)
            browser.close()
            return response
