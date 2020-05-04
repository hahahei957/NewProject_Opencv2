# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

class AiqiyiSpiderMiddleware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(spider.settings.get("USER_AGENT_LSIT"))