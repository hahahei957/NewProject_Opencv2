# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


"""进行数据处理和保存，但需要在setting.py文件中开启"""

import logging

logger = logging.getLogger(__name__)


class MyspderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "itcast":
            # if item["come_from"]=="itcast":
            logger.warning(item)
            # print(item)

        return item

    # def process_item1(self, item, spider):
    #     if spider == "itcast1":
    #         print(item)
    #
    #     return item

class MyspderPipeline1(object):
    def process_item(self, item, spider):
        if spider == "itcast1":
            print(item)

        return item