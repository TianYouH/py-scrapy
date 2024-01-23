# scrapy 测试项目

## 创建项目

在期望根目录控制台执行脚本`scrapy startproject tutorial`

- scrapy.cfg: 项目的配置文件，现在可以先忽略。
- tutorial: 该项目的python模块。 
  - items.py: Item对象可以保存爬取到的数据、相当于存储爬取到的数据的容器。 对于爬取到的的数据,需要提取出我们关注的结构化的信息,以便于对数据的管理。
  - pipelines.py: 主要用于接收提取出来的项目(item),接收后,会对这些item进行处理常见的处理方式主要有:清洗、验证、导出到外部文件、存储到数据库等。
  - settings.py: settings文件为爬虫项目的设置文件，主要是爬虫项目的一些设置信息。例如,启用了pipelines，需要把settings中相关代码的注释取消主要修改点：(为了反爬)
  - middlewares.py：爬虫项目的中间件文件。
  - spiders: 定义爬取的动作及分析某个网页(或者是有些网页)的地方。例如,写Xpath语句或者正则表达式,及爬取多页数据等

## 创建spider

在当前项目下执行`scrapy genspider quotes quotes.toscrape.com`

### 修改QuotesSpider

将地址更新为要爬网站地址，便携初代测试代码
```python
    start_urls = ["https://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath("./span[@class='text']/text()").get(),
                'author': quote.xpath("./span/small[@class='author']/text()").get(),
                'tags': quote.xpath("./div[@class='tags']/a[@class='tag']/text()").getall()
            }
        # 增加多页爬取逻辑
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url is not None:
            yield scrapy.Request("https://quotes.toscrape.com" + next_url)
```
执行脚本并导出json`scrapy crawl  quotes -O test.json`

### 使用 Items 结构

配置结构
```py
# tutorial/items.py
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```
# 使用
```py
# tutorial/spiders/quotes.py
from tutorial.items import TutorialItem

for quote in response.xpath("//div[@class='quote']"):
    tutorial_item = TutorialItem()
    tutorial_item['text'] = quote.xpath("./span[@class='text']/text()").get()
    tutorial_item['author'] = quote.xpath("./span/small[@class='author']/text()").get()
    tutorial_item['tags'] = quote.xpath("./div[@class='tags']/a[@class='tag']/text()").getall()
    yield tutorial_item
```