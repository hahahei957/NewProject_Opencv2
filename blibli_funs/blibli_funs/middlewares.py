# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


class RandomUserAgentList:
    def process_requset(self, request, spider):
        user_agent = random.choice(spider.setting.get("USER_AGENT_LIST"))
        request.headers["User-Agent"] = user_agent



