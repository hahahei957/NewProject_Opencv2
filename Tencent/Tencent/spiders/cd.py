# -*- coding: utf-8 -*-
import scrapy


class CdSpider(scrapy.Spider):
    name = 'cd'
    allowed_domains = ['..']
    start_urls = ['http://../']

    def parse(self, response):
        pass
