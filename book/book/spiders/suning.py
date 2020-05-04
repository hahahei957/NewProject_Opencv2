# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re

"""scrapy框架deepcopy         !!!!!!!!!!!
问题：
meta传递值，有时候当前爬虫解析出来的数据需要重复抓取，获取到的值有时需要传递给下一个函数
但是 items= response.meta['item'] 接收的时候一直是同样的值

-->      我感觉当有多层for循环嵌套的时候，尽量全用深拷贝，否则获取的数据可能出现好多name与href或者src这样的标签与标签不匹配的问题    <--

解决：
在yield的时候，meta参数的值做深度拷贝就可以了"""

class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']
    print(1, "-----------------")               # 在执行完这一句之后，parse函数之前，程序会去执行middlewares函数，所以我们可以在这里先用selenium请求得到cookies
    def parse(self, response):

        # 获取属性时才用extract_first或extract，在提取元素对象时，就不要用了
        div_list = response.xpath("//div['left-menu-container']/div[@class='menu-sub']")
        for div in div_list:
            # print(div, "=========================")

            # 获取属性时才用extract_first或extract，在提取元素对象时，就不要用了
            p_list = div.xpath("./div[@class='submenu-left']/p")
            for i in range(len(p_list)):
                item = dict()
                print("_____________________")

                # 之前一直报错，是因为这里的i我是直接添加进了p[i+1]的形式，而这样会导致i变成一个字符串，而非我们的变量i
                item["sort"] = div.xpath("./div[@class='submenu-left']/p[{}+1]/a/text()".format(i)).extract_first()

                li_list = div.xpath(".//div[@class='submenu-left']/ul[{}+1]/li".format(i))
                for li in li_list:
                    item["tag"] = li.xpath("./a/text()").extract_first()
                    item["href"] = li.xpath("./a/@href").extract_first()
                    # print(item)

                    yield scrapy.Request(
                        url=item["href"],
                        callback=self.parse_book_list,
                        # 我感觉当有多层for循环嵌套的时候，尽量全用深拷贝，否则获取的数据可能出现好多name与href或者src这样的标签与标签不匹配的问题
                        meta={"item": deepcopy(item)}
                    )

    # 获取子页的图书列表
    def parse_book_list(self, response):
        item = response.meta['item']

        li_list = response.xpath("//ul[@class='clearfix']/li")
        for li in li_list:
            item["title"] = li.xpath(".//a/img/@alt").extract_first()

            item["detail_href"] = li.xpath(".//div[@class='res-img']//a/@href").extract_first()

            # 这里注意有时候报错的原因也可能是：我们要xpath的内容在element中的位置和实际得到响应中要素的位置不一样
            item["img"] = "https:" + li.xpath(".//a/img/@src2").extract_first()
            # print(item)
            # print(11111111111)
            # 这里取详情页的时候，要注意用深拷贝，防止
            # 获取详情页的评价信息
            # print("https:" + item["detail_href"])
            yield scrapy.Request(
                url="https:" + item["detail_href"],
                callback=self.parse_detail_comment_updata,  # 只拿了部分评论
                # 我感觉当有多层for循环嵌套的时候，尽量全用深拷贝，否则获取的数据可能出现好多name与href或者src这样的标签与标签不匹配的问题
                meta={"item": deepcopy(item)}
            )

        # 如果取不到下一页的值，extact_first会返回空值
        next_url = response.xpath("//a[@title='下一页']").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                url="https://list.suning.com/" + next_url,
                callback=self.parse_book_list,
                meta={"item": deepcopy(item)}
            )
    # 仅仅得到图书评论的简单版本
    def parse_detail_comment(self, response):
        item = response.meta["item"]
        print(2222222)
        # print(response.text)

        "                    ---------------------------->              <-----------------------------"
        # 这里我在Network中找到的text是 "查看全部评论&gt;"  而在element中找到的是  "查看全部评论>"
        # 这里我们应该使用element中的来xpath，因为很可能 ">" 在response中的表现形式是 "&gt;"
        div_list = response.xpath('//a[text()="查看全部评论>"]/@href').extract_first()
        # TODO:这里的div是获取不到的，因为在加载图书详情页时，评论并没有一起加载出来，并且评论中下一页的请求，也是在本页面更新的，都是ajax请求，明天掌握ajax来解决此问题
        # TODO:  百度搜索 -->  scrapy框架处理ajax
        # for div in div_list:
        #     item["detail_comment"] = div.xpath(".//div[@class='topic-body']/p/text()").extract_first()
        #     print(111111111111111111111111)
        item["detail_comment_href"] = div_list
        print(item)

    # 通过搜寻参数的到评论ajax的url
    def parse_detail_comment_updata(self, response):
        item = response.meta["item"]
        # print(2222222)
        div_list = "https" + response.xpath('//a[text()="查看全部评论>"]/@href').extract_first()
        id = re.findall("/general(-\d*-\d*-\d-)total\.htm", div_list)
        target_ajax_url = "https://review.suning.com/ajax/cluster_review_lists/general-" + id[0] + "total-1-default-10-----reviewList.htm?callback=reviewList"
        # TODO:这里的div是获取不到的，因为在加载图书详情页时，评论并没有一起加载出来，并且评论中下一页的请求，也是在本页面更新的，都是ajax请求，明天掌握ajax来解决此问题
        # TODO:  百度搜索 -->  scrapy框架处理ajax
        # for div in div_list:
        #     item["detail_comment"] = div.xpath(".//div[@class='topic-body']/p/text()").extract_first()
        #     print(111111111111111111111111)
        item["user_of_commenter_url"] = target_ajax_url
        print(item)
        print(item["user_of_commenter_url"])

"""https://review.suning.com/ajax/cluster_review_lists/general--000000011429483006-0070129646-total-1-default-10-----reviewList.htm?callback=reviewList
https://review.suning.com/cmmdty_review/general-000000011429483006-0070129646-1-total.htm"""



