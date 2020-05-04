# -*- coding: utf-8 -*-
import scrapy
import re
import zlib
from copy import deepcopy

# https://cmts.iqiyi.com/bullet/tv_id[-4:-2]/tv_id[-2:]/tv_id_300_x.z
# https://cmts.iqiyi.com/bullet/视频编号的倒数4、3位/视频编号的倒数2、1位/视频编号_300_序号.z
# 弹幕文件每5分钟（300秒）向服务器请求一次，故每集弹幕文件数量等于视频时间除以300之后向上取整，实际编程时这里可以简单处理

# https://pcw-api.iqiyi.com/video/video/hotplaytimes/14774604600,14486883200,14191578400,13919837200,13629991300,13342399900,13028439200,12578293100,12333995600/
# 可以通过检索视频的vid查询视频的热度


class DanmuSpider(scrapy.Spider):
    name = 'danmu'
    allowed_domains = ['iqiyi.com']
    keyword = input("请输入要爬取弹幕的系列视频的名字：")
    start_urls = [f'https://so.iqiyi.com/so/q_{keyword}']

    # 从我们搜索keyword关键词得到结果中，xpath获取排在第一个大类的url
    def parse(self, response):
        item = dict()
        # 本来打算一次性直接爬取歌手所有的视频的tvid，好收集弹幕，但最后没找到合适的url，所以我们申请每一期视频的url，再得到vid，虽然麻烦，但值得一试
        item['main_url'] = response.xpath("//div[@desc='card'][1]//a[@class='main-tit']/@href").extract_first()
        item['mian_title'] = response.xpath("//div[@desc='card'][1]//a[@class='main-tit']/@title").extract_first()

        # 下面这些代码就是 本来打算一次性直接爬取歌手所有的视频的tvid，好收集弹幕，但最后没找到合适的url，所以我们申请每一期视频的url，再得到vid，虽然麻烦，但值得一试
        # for i, temp in enumerate(item['contains_vid']):
        #     vid = re.findall("tvid=(\d*?)&aid=", temp)
        #     url = f"https://cmts.iqiyi.com/bullet/72/00/{vid}_300_1.z"
        #     yield scrapy.Request(
        #         url=url,
        #         callback=self.detail_danmu,
        #         meta={"title":item['mian_title'][i]}
        #     )

        # 请求第一个大类的url
        url = "https:"+item['main_url']
        yield scrapy.Request(
            url=url,
            callback=self.every_drama,
            meta={"item":deepcopy(item)}
        )

    # xpath获取第一个大类下所有剧集的url
    def every_drama(self, response):
        item = response.meta['item']
        item["every_darma_url"] = response.xpath("//div[contains(@class,'piclist')]//a[contains(@rseat,'_sub1_tuwentitle')]/@href").extract()
        print("====================")
        print(item['every_darma_url'])
        print("=====================")

        for url in item["every_darma_url"]:   # 因为这里请求了好几重下一级，而且item传递了好几次，在我们没使用deepcopy的时候，
            url = "https:" + url
            # 请求每一个剧集的url
            yield scrapy.Request(
                url=url,
                callback=self.get_vid,
                meta={"item":deepcopy(item)}
            )

    # 在每一个剧集的url中获取该剧集的tvid，以便于我们通过这个tvid请求得到所有的弹幕
    def get_vid(self, response):
        item = response.meta['item']
        content = response.xpath("//meta[@name='apple-itunes-app']/@content").extract_first()
        # 通过findall得到的是一个列表，所以我们需要取其的第一项从而转换成一个int型的数据
        tvid = re.findall("tvid=(\d*?)&aid=", content)[0]

        # 下面这个xpath用的很好，看一下
        # item['title'] = response.xpath("//span[@class='title-mark']/../a/@title").extract_first()
        item['title'] = response.xpath("//meta[@name='title']/@content").extract_first()
        print(tvid)

        # 组装要请求弹幕的url  ==>  https://cmts.iqiyi.com/bullet/72/00/13919837200_300_1.z
        # 这里关于切片的部分要好好跟人家学学，这里的[-2:]使用的很好
        url = "https://cmts.iqiyi.com/bullet/"+str(tvid[-4:-2])+"/"+str(tvid[-2:])+"/"+str(tvid)+"_300_1.z"
        yield scrapy.Request(
            url=url,
            callback=self.danmu,
            meta={"item":deepcopy(item)}
        )

    def danmu(self,response):
        item = response.meta['item']

        # scrapy中response.body 与 response.text区别
        # body http响应正文， byte类型
        # text 文本形式的http正文，str类型，它是response.body经过response.encoding经过解码得到
        # response.text = response.body.decode(response.encoding)
        res_byte = bytearray(response.body)            # 因为得到的就是byte类型的数据，所以我认为这里的转化其实是不需要的
        xml = zlib.decompress(res_byte, 15+32).decode("utf-8")
        # print(xml)
        content_list = re.findall("<content>(.*?)</content>", xml)

        # with open(file=item['title']+'.txt', 'a', encoding='utf-8') as f:
        # 由于如果前面使用关键字赋值就需要后面的都使用，这里只有前面的使用了一个关键字参数赋值，因此报错：SyntaxError: positional argument follows keyword argument
        with open(item['title']+'.txt', 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(content+"\r\n")
            f.close()
        print(f"{item['title']}爬取完毕")

    def detail_danmu(self, response):
        title_name = response.meta['title']
        danmu = zlib.decompress(response.text, 15+32).decode("utf-8")
        pass