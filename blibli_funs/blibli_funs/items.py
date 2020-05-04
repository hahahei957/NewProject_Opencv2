# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlibliFunsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    _id = scrapy.Field()       # 由于我们这里貌似必须要自己设置_id， 所以我们用表示用户的mid来代替_id
    funs = scrapy.Field()
