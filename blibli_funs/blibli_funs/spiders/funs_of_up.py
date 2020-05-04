# -*- coding: utf-8 -*-
import scrapy
import json
from blibli_funs.items import BlibliFunsItem
import time
import random                                   # 通过sleep的方式访问，防止被检测出来，把我们的ip封掉

class FunsOfUpSpider(scrapy.Spider):
    name = 'funs_of_up'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=1&copy_right=-1&cate_id=76&page=1&pagesize=20&jsonp=jsonp&time_from=20200311&time_to=20200318']

    def parse(self, response):
        content_dict = json.loads(response.text, encoding="utf-8")

        ups_list = list()                                  # 保存B站up主的名字
        next_page = 2
        try:
            ups_list = response.meta["ups_list"]
            next_page = response.meta["next_page"] + 1
            print("第{}页往后的爬虫开始。。。".format(next_page-1))
        except Exception as result:
            print("第一页的爬虫开始。。。")
        for mesg in [content_dict["result"][i] for i in range(20)]:
            item = BlibliFunsItem()
            item["author"] = mesg["author"]
            item["_id"] = mesg["mid"]                               # 由于我们这里貌似必须要自己设置_id， 所以我们用表示用户的mid来代替_id
            if item["author"] not in ups_list:
                ups_list.append(item["author"])
                # 通过唯一标识up主的mid，从子页中请求到粉丝的数量
                yield scrapy.Request(
                    url="https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(item["_id"]),
                    callback=self.detail_page,
                    meta={"item": item}
                )

        # 请求下一页
        next_url = "https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=1&copy_right=-1&cate_id=76&page={}&pagesize=20&jsonp=jsonp&time_from=20200311&time_to=20200318".format(next_page)
        yield scrapy.Request(
            url=next_url,
            callback=self.parse,
            meta={"ups_list":ups_list, "next_page":next_page}
        )

    def detail_page(self, response):
        item = response.meta["item"]
        item["funs"] = json.loads(response.text)["data"]["follower"]
        print("--------------", item)

        time.sleep(random.random()*3)           # 通过sleep的方式访问，防止被检测出来，把我们的ip封掉  ==>  这句写的很好

        yield item