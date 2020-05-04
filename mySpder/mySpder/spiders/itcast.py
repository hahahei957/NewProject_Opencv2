# -*- coding: utf-8 -*-
import scrapy
import logging

"""创建scrapy框架： scrapy startproject mySpyder(也就是框架名) -->  cd mySpyder  --> """
""" -->  (初始化生成项目文件的方式)   scrapy genspider itcast(项目名) itcast.cn(允许爬取的项目范围)"""
"""执行时，用 scrapy crawl itcast(也就是项目名)"""


# 在使用logger打印日志时，通过__name__可以说明当前打印的位置是在哪个.py文件
logger = logging.getLogger(__name__)


class ItcastSpider(scrapy.Spider):
    name = 'itcast'  # 爬虫名
    allowed_domains = ['itcast.cn']  # 允许爬虫的范围
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']  # 最开始请求的url地址

    def parse(self, response):
        # 处理start_url对应的响应
        li_list = response.xpath("//div[@class='tea_con']//li")

        # 分组，不能通过content了
        for li in li_list:
            item = dict()
            item['name'] = li.xpath(".//h3/text()").extract_first()  # 相当于.extract()[0]，如果结果为空时，就会返回None
            item['title'] = li.xpath(".//h4/text()").extract_first()
            # print(item)

            # 相当于print 但是它多了打印日志的功能
            logger.warning(item)

            yield item

