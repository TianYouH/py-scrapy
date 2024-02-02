# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class TutorialPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['quotes']
    def process_item(self, item, spider):
        # self.db.quotes2.insert_one(dict(item))
        self.db.quotes2.replace_one({'text': item['text']}, dict(item), True)
        pass
        # return item
