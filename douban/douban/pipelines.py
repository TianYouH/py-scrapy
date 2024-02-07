# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql

class ExcelPipeline:

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

class DBPipeline:

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", user="test", 
                                    password="123456", database="spider", 
                                    charset="utf8")
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        # self.conn.commit()
        if len(self.data) > 0:
            self._write_to_db()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get("title", "")
        rate = item.get("rate", 0)
        comment = item.get("comment", "")
        quote = item.get("quote", "")
        '''
        # 保存到(单条)数据库
        self.cursor.execute("insert into tp_top_movie (title, rate, comment, quote) values(%s, %s, %s, %s)", 
                            (title, rate, comment, quote))
        '''
        # 保存到(批量)数据库
        self.data.append((title, rate, comment, quote))
        if len(self.data) >= 100:
            self._write_to_db()
            self.data.clear()
        return item

    def _write_to_db(self):
        self.cursor.executemany("insert into tp_top_movie (title, rate, comment, quote) values(%s, %s, %s, %s)", self.data)
        self.conn.commit()
