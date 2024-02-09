import scrapy
from douban.items import MovieItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]

    def start_requests(self):
        # 从第一页开始爬取
        yield scrapy.Request("https://movie.douban.com/top250")
        # 从第一页到第十页
        # for i in range(0, 10):
        #     url = f"https://movie.douban.com/top250?start={i*25}"
        #     yield scrapy.Request(url)

    def parse(self, response):
        list_items = response.css("#content > div > div.article > ol > li")
        for item in list_items:
            detail_url = item.css(".hd a::attr(href)").extract_first()
            movie_item = MovieItem()
            # 电影名
            movie_item["title"] = item.css(".hd span::text").extract_first()
            # 电影评分
            movie_item["rate"] = item.css(".rating_num::text").extract_first()
            # 电影评价人数
            movie_item["comment"] = item.css(".star span::text").extract()[-1]
            # 电影描述
            movie_item["quote"] = item.css(".quote span::text").extract_first()
            # yield movie_item
            yield scrapy.Request(detail_url, callback=self.parse_detail, cb_kwargs={"item": movie_item})

    def parse_detail(self, response, **kwargs):
        movie_item = kwargs["item"]
        movie_item["duration"] = response.css("#info span[property='v:runtime']::text").extract_first()
        movie_item["intro"] = response.css("#link-report-intra span[property='v:summary']::text").extract_first()
        yield movie_item