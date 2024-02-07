# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class DoubanSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# 将cookies字符串转换为字典
def get_cookies_dict(cookies):
    cookies_dict = {}
    for cookie in cookies.split(";"):
        key, value = cookie.split("=", 1)
        cookies_dict[key] = value
    return cookies_dict

cookies_str='ll="118245"; bid=UxTmV2w0cDE; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1707302611%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_id.100001.8cb4=aecdd600ac1cc134.1707302611.; _pk_ses.100001.8cb4=1; __utma=30149280.1748020854.1706885974.1706971324.1707302612.3; __utmc=30149280; __utmz=30149280.1707302612.3.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19194; ck=qZJi; ps=y; __utmt=1; __utmb=30149280.5.10.1707302612'
COOKIES_DICT = get_cookies_dict(cookies_str)

class DoubanDownloaderMiddleware:
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
        # 设置cookies 记得去settings.py中设置COOKIES_ENABLED = True 否则不生效
        # 还要启用 DOWNLOADER_MIDDLEWARES = {'douban.middlewares.DoubanDownloaderMiddleware': 543,}
        # request.cookies = COOKIES_DICT
        # request.mateta['proxy'] = "http://"
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
        spider.logger.info("Spider opened: %s" % spider.name)
