# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl

class DoubanPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = "豆瓣电影Top250"
        self.sheet.append(["电影名", "评分", "评价人数", "描述"])

    def close_spider(self, spider):
        self.wb.save("豆瓣电影Top250.xlsx")

    def process_item(self, item, spider):
        line = [item["title"], item["rate"], item["comment"], item["quote"]]
        self.sheet.append(line)
        return item
