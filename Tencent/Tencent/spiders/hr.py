# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem           # 这里报的错误不用管
import json
import logging
import random

logger = logging.getLogger(__name__)
GLOB_I = 1

class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?&pageIndex=1&pageSize=10']

    def parse(self, response):
        item = TencentItem()

        # 处理响应为json的文段的方式：
        # response.body.decode()应该也可以提取响应页面的字段
        content_dict = json.loads(response.text)

        position_list = content_dict["Data"]["Posts"]

        for position in position_list:

            # 解决_id 重复的问题
            item["_id"] = "title" + str(random.randint(1, 1000))
            # item中的键名一定要在items.py文件夹下面声明一下
            item["post"] = position["RecruitPostName"]
            item["LocationName"] = position["LocationName"]
            logger.warning(item)
            yield item

        global GLOB_I
        GLOB_I += 1
        # 找到下一页的url地址
        next_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?&pageIndex={}&pageSize=10'.format(GLOB_I)
        if GLOB_I <= 477:
            # 通过scrapy.Request发送请求
            yield scrapy.Request(
                next_url,
                # 表示当前url对应的响应交给谁处理，又因为当前这个方法self.parse和我们要进行的提取数据处理方式一样，
                # 否则我们就要重新定义一个方法如parse1 来处理我们的响应 如callback=self.parse1
                callback=self.parse,
                # meta = {"it" = item}     # 通过meta可以往子方法也就是self.parse，传数据(例如键名为it的指向item的键值对等)
            )

    def parse1(self, response):
        # 通过meta就可以实现数据或者说item在不同解析函数中传递的需求了
        dict = response.meta["it"]