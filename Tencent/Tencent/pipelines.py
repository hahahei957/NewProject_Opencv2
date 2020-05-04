# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from pymongo import MongoClient

# 通过pymongo实现piplines对于数据的处理和保存
""" _id重复的问题：
https://blog.csdn.net/Refrain__WG/article/details/82287724  https://blog.csdn.net/qq_43391383/article/details/87094991  -->  
 pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: tencent.hr index: _id_ dup key: { : ObjectId('5e4f4e077c84f48f31bf8c77') }"""
client = MongoClient(host="127.0.0.1", port=27017)
collection = client["tencent"]["hr"]

logger = logging.getLogger(__name__)


class TencentPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "hr":
            # 通过mongodb实现数据的保存
            collection.insert(item)
            logger.warning(item)

            return item
