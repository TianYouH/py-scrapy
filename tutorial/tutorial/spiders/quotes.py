from tutorial.items import TutorialItem
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            tutorial_item = TutorialItem()
            tutorial_item['text'] = quote.xpath("./span[@class='text']/text()").get()
            tutorial_item['author'] = quote.xpath("./span/small[@class='author']/text()").get()
            tutorial_item['tags'] = quote.xpath("./div[@class='tags']/a[@class='tag']/text()").getall()
            yield tutorial_item
        # 增加多页爬取逻辑
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url is not None:
            yield scrapy.Request("https://quotes.toscrape.com" + next_url)

