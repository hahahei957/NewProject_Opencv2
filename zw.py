# -*- coding: utf-8 -*-
import scrapy


class ZwSpider(scrapy.Spider):
    name = 'zw'
    allowed_domains = ['cnki.net']
    start_urls = ['http://cnki.net/']

    def parse(self, response):
        pass
