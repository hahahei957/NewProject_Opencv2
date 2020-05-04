# -*- coding: utf-8 -*-
"""
这次这个是一般情况,也就是无法用cookies重复登陆，必须每次都要重复登陆的页面
而且具体实现过程，比login_blibli更加高级全面，更加完善
"""
import scrapy
from selenium import webdriver

# scrapy信号相关库
from scrapy import signals

from pydispatch import dispatcher

class LoginBlibli02Spider(scrapy.Spider):
    name = 'login_blibli_02'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']

    def __init__(self):
        super(LoginBlibli02Spider, self).__init__()


    def parse(self, response):
        pass
