# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 通过 scrapy genspider -t crawl tb_crawl baidu.com 这句话实现crawlspider的创建
class TbCrawlSpider(CrawlSpider):
    name = 'tb_crawl'
    allowed_domains = ['baidu.com']
    start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=%E6%9D%8E%E6%AF%85&pn=0&']

    rules = (
        # 貌似是用来匹配整个字符串的，而开头的"http://"这类的东西，在请求时会被自动的添加上  ==  /p/6469173522?lp=5028&amp;mo_device=1&amp;is_jingpost=0
        Rule(LinkExtractor(allow=r'/p/\d+\?lp=\d+&mo_device=1&is_jingpost=0'), callback='parse_detail_item'),

        # 最近贴吧改了，下一页貌似是通过js，所以是通过调整参数找规律获得下一页的url,如果像这样url不是通过response找出的话，那是不能使用crawlspider这种爬虫方式的

        # Rule(LinkExtractor(allow=r'/p/\d+\?lp=\d+&mo_device=1&is_jingpost=0'), follow=True)
    )


    def parse_detail_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['img'] = response.xpath("//span[@class='wrap pbimgwapper']/img/@src").extract()
        """ response.xpath("//div[@class='pb_img_item']/img/@src").extract() if len(item['author_img'])>0 else """
        item['author_img'] = response.xpath("//div[@id='pb_imgs_div']//img/@src").extract()
        item['author_img'] = response.xpath("//div[@class='pb_img_item']/@data-url").extract() if len(item['author_img']) == 0 else item['author_img']
        print(item)
        # return item
