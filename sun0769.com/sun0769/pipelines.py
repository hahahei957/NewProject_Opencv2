# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import re

logger = logging.getLogger(__name__)

class Sun0769Pipeline(object):
    def process_item(self, item, spider):
        """  ====>        看一看，学习一下这个函数<==="""
        """   看一看学习一下这个函数对于正则的使用 --》 self.process_recv_mesg"""
        item["detail_message"] = self.process_recv_mesg(item["detail_message"])
        logger.warning(item)
        return item

    # 这个函数是用来对item["detail_mesg"]获取出来的文本数据进行清洗的
    def process_recv_mesg(self,mesg_list):

        # \s对应正则中的空字符串，re.sub是将正则匹配出来的数据替换成后面匹配出来的
        mesg_list = [re.sub("\r\n|\t|\xa0|\n|\s", "", i) for i in mesg_list]
        # 出去列表中的空字符串
        mesg_list = [i for i in mesg_list if len(i)>0]
        return mesg_list


