# -*- coding: utf-8 -*-
import scrapy


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['https://tieba.baidu.com/']
    start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=李毅&fr=search']

    def parse(self, response):
        li_list = response.xpath("//ul[@id='thread_list']/li")

        for li in li_list:
            pass
        pass
