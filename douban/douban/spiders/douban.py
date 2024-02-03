import scrapy
from douban.items import MovieItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]

    def start_requests(self):
        for i in range(0, 10):
            url = f"https://movie.douban.com/top250?start={i*25}"
            yield scrapy.Request(url)

    def parse(self, response):
        list_items = response.css("#content > div > div.article > ol > li")
        for item in list_items:
            movie_item = MovieItem()
            # 电影名
            movie_item["title"] = item.css(".hd span::text").extract_first()
            # 电影评分
            movie_item["rate"] = item.css(".rating_num::text").extract_first()
            # 电影评价人数
            movie_item["comment"] = item.css(".star span::text").extract()[-1]
            # 电影描述
            movie_item["quote"] = item.css(".quote span::text").extract_first()
            yield movie_item