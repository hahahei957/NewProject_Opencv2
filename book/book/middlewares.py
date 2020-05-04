# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
# 在执行完这一句之后，parse函数之前，程序会去执行middlewares函数，所以我们可以在这里先用selenium请求得到cookies

# 在发送请求之前，先执行这个函数    ,也就程序在执行到parse方法时，才会先调用这里，所以我们可以在这里先用selenium请求得到cookies
# 这个函数也可以添加随机代理、cookies
class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        print(2, "-----------------------")
        # random.choice这个函数也要多多了解
        user_agent = random.choice(spider.settings.get('USER_AGENT_LIST'))
        request.headers['User-Agent'] = user_agent


# 这句貌似是在收到响应之后再执行的（不太确定）
class CheckUserAgent:
    def process_response(self, request, response, spider):
        print(request.headers['User-Agent'])
        return response                                       # 这里必须return response或者return request