# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random


class UseOfSeleniumSpiderMiddleware(object):
    # 后面这句理解是不对的：(之所以在这里设置cookies的原因，是因为每次请求都要先经过这里，所以在这里设置cookies是最合适不过的了）
    # 我觉得在这里设置cookies啥的是因为，这样可以让我们每次请求的cookies、代理ip、user-agent都有所不懂，从而确保不被检测出爬虫行为
    # 如果一直用同一个cookies、ip和user-agent的话，就没必要在用middlewares了
    def process_request(self, request, spider):
        # 设置user-agent
        print(2, "---------------------------------------------------------------")
        request.headers["User-Agent"] = random.choice(spider.settings.get("USERAGENT_LIST"))
        # 设置cookies
        cookie_list = [temp["name"] + ":" + temp["value"] for temp in spider.seleniumCookies]
        cookMap = dict()

        # 将selenium获得的cookies的格式转化为scrapy能识别的cookies格式
        # 注：selenium获得的cookies的格式就是network的cookies表中的格式
        for cookie in cookie_list:
            str = cookie.split(':')
            cookMap[str[0]] = str[1]       # 弄成字典的键值对的形式
        print("-----------------------------------------")
        print(f"cookMap = {cookMap}")
        # 中间件，对Request进行加工
        # 开始用这个转换后的cookie重新构造Request，从源码中来看Request构造的原型
        # E:\Miniconda\Lib\site-packages\scrapy\http\request\__init__.py
        request.cookies = cookMap  # 让这个带有登录后cookie的Request继续爬取



