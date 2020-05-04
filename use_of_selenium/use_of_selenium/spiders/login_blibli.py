# -*- coding: utf-8 -*-
"""https://blog.csdn.net/zwq912318834/article/details/79870432"""
import scrapy
from selenium import webdriver
import time
from scrapy import signals              # scrapy 信号相关库

from pydispatch import dispatcher       # scrapy最新采用的方案

class LoginBlibliSpider(scrapy.Spider):
    name = 'login_blibli'
    allowed_domains = ['bilibili.com/']
    start_urls = ['https://api.bilibili.com/x/web-interface/nav']

    def __init__(self):
        super(LoginBlibliSpider, self).__init__()
        print(33333333333333333333)

        # 这个路径指向我们电脑使用的cookies以及localstorage等一大些登陆信息，从而可以很方便的实现
        profile_directory = r'--user-data-dir=C:\Users\acer\AppData\Local\Google\Chrome\User Data'
        # 实例化一个浏览器对象(实例化一次)
        options = webdriver.ChromeOptions()
        options.add_argument(profile_directory)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get("https://space.bilibili.com/")
        self.seleniumCookies = self.driver.get_cookies()
        print(f"seleniumCookies = {self.driver.get_cookies()}")
        # time.sleep(3)
        # self.driver.quit()

        # 设置信号量，当收到spider_closed信号时，调用mySpiderCloseHandle方法，关闭chrome
        dispatcher.connect(receiver=self.mySpiderCloseHandle,
                           signal=signals.spider_closed
                           )

    # 信号量处理函数：关闭chrome浏览器
    def mySpiderCloseHandle(self, spider):    # 不知道为啥，例子中这里给了参数spider
        self.driver.quit()

    print("1", "-------------------")

    def parse(self, response):
        print(response.text)




