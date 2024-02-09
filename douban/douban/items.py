# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    title = scrapy.Field() # 电影名
    rate = scrapy.Field() # 电影评分
    comment = scrapy.Field() # 电影评价人数
    quote = scrapy.Field() # 电影描述
    duration = scrapy.Field() # 电影时长
    intro = scrapy.Field() # 电影简介

