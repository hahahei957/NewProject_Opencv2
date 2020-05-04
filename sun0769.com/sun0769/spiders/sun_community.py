# -*- coding: utf-8 -*-
import scrapy
from sun0769.items import Sun0769Item
import logging

logger = logging.getLogger(__name__)

class SunCommunitySpider(scrapy.Spider):
    name = 'sun_community'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://bbs.sun0769.com/forum.php?mod=forumdisplay&fid=131']

    def parse(self, response):

        # 不要在一开始就初始化item，而是在每次循环中初始化
        # item = Sun0769Item()

        logger.warning("---------------------- 1 -----------------------------")
        tbody_list = response.xpath("//table[@id='threadlisttableid']/tbody")
        logger.warning("---------------------- 2 -----------------------------")
        for tbody in tbody_list:

            # 这个item一定要在每次循环中都初始化一次，而不是在开头，否则会失败
            item = Sun0769Item()

            # if tbody.xpath("./@id") != "separatorline" and tbody.xpath("./@id") != "stickthread_1964481" and tbody.xpath("./@id") != "stickthread_1944703":
            temp_str = str(tbody.xpath("./@id").extract_first())
            print(temp_str,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            if temp_str[1] == 'o':
                item["title"] = tbody.xpath(".//th/a[2]/text()").extract_first()
                item["href"] = "http://bbs.sun0769.com/" + tbody.xpath(".//th/a[2]/@href").extract_first()
                item["writer"] = tbody.xpath(".//td[@class='by']//a/text()").extract_first()
                item["time"] = tbody.xpath(".//td[@class='by']/em/span/text()").extract_first()
                # logger.warning(item)
                # 请求子页(也就是详情页的文段)
                yield scrapy.Request(
                    url=item["href"],
                    callback=self.parse_detail,
                    meta={"item": item}
                )

        # 翻页 翻页应该在循环结束之后
        """这两句 xpath 都写的挺好的"""
        """response.xpath("//a[text()='下一页']/@href").extract_first()  得到的结果类型是str"""
        # next_url = response.xpath("//span[@id='fd_page_bottom']/a[last()]/@href").extract_first()
        next_url = "http://bbs.sun0769.com/" + response.xpath("//a[text()='下一页']/@href").extract_first()

        yield scrapy.Request(
            url=next_url,
            callback=self.parse
            # 这里就不用继续给下一个传item了，这里要重新创建一个item，重新按照parse的方式去爬下一页
        )

    def parse_detail(self, response):
        item = response.meta["item"]

        logger.warning("-------------------------------33-------------------------------------------")
        # xpath关于contains的使用
        detail_list = response.xpath("//td[contains(@id,'postmessage_')]")
        logger.warning("-------------------------------44----------------------")

        """  ========================》 下面自己写的for循环，以及后面yield为啥放在for循环外边的解释，都好好看一看  《================"""
        # for detail in detail_list:
        #
        #     # 回去看看该网站中detail的文本数据在很多个例标签中，要想通过for循环取数据是几乎不可能的
        #     item["detail_message"] = detail.xpath(".//text()").extract_first()
        #     item["detail_img"] = detail.xpath(".//img/@src").extract_first()
        #     # logger.warning(item)


        # # yield也应该在前面的for循环外面，否则，同一个新闻对应的detail会向yield发送多次，
        # # 同理，在for循环中使用打印item的命令，也会让一条信息打印多次
        # yield item


        """ ================》 下面是源码给出的提取详情页数据的xpath语句，十分的优秀，多看几遍  《================"""

        # extract():这个方法返回的是一个数组list，，里面包含了多个string，如果只有一个string，则返回['ABC']这样的形式。
        # extract_first()：这个方法返回的是一个string字符串，是list数组里面的第一个字符串。
        item["detail_message"] = response.xpath("//td[contains(@id,'postmessage_')]//text()").extract()
        item["detail_img"] = response.xpath("//td[contains(@id,'postmessage_')]//img/@src").extract()

        item["detail_img"] = ["http://wz.sun0769.com" + i for i in item["detail_img"]]

        yield item