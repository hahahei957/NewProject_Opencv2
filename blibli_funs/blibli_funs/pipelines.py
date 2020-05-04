# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


client = MongoClient(host="127.0.0.1", port=27017)
collection = client["blibli"]["up"]

class BlibliFunsPipeline(object):
    def process_item(self, item, spider):
        content = "author : " + item["author"] + "followers : " + str(item["funs"]) + "\r\n"
        print(item)
        with open("./B站up主的名字和粉丝数量.txt", "a", encoding="utf-8") as f:
            f.write(content)
            f.close()
        collection.insert_one(item)                       # 由于Mongondb不给配置_id，我们的解决方案是自己给他的字典中配置一个_id
        return item
