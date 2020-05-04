# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class ShandongSpider(CrawlSpider):
    name = 'shandong'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://sd.weather.com.cn/']

    rules = (
        # 下面这个正则虽然匹配到了url，但我们要匹配的部分中，仅需要其中的url向<a href=这样的内容是不需要，对目标部分加上小括号也没用
        # Rule(LinkExtractor(allow=r'<a href="(.*?)" target="_blank">'), callback='parse_item'),
        # 该过程是通过正则匹配得到一个url列表，在对其中的每一个分别发送请求，call给parse_item使用
        Rule(LinkExtractor(allow=r'http://www\.weather\.com\.cn/weather/\d+\.shtml'), callback='parse_item'),    # rules中必须有逗号，否则就不是列表了
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        city = re.findall(r"便捷查询(.*?)今日天气", response.text)
        item["city"] = city
        day_list = response.xpath("//li[contains(@class,'sky skyid')]/h1/text()").extract()
        wea_list = response.xpath("//li[contains(@class,'sky skyid')]/p[@class='wea']/text()").extract()
        temperature_list = response.xpath("//li[contains(@class,'sky skyid')]/p[@class='tem']/span/text()").extract()
        for i in range(len(wea_list)):
            item[day_list[i]] = wea_list[i] + ":" + temperature_list[i]
        print(item)
        return item
