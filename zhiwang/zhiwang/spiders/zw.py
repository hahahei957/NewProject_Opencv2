# -*- coding: utf-8 -*-
import scrapy
import time
import random

"""通俗来说， robots.txt 是遵循 Robot协议 的一个文件，它保存在网站的服务器中，它的作用是，告诉搜索引擎爬虫，本网站哪些目录下的网页 不希望 你进行爬取收录。
在Scrapy启动后，会在第一时间访问网站的 robots.txt 文件，然后决定该网站的爬取范围。当然，我们并不是在做搜索引擎，而且在某些情况下我们想要获取的内容恰恰是被
 robots.txt 所禁止访问的。所以，某些时候，我们就要将此配置项设置为 False ，拒绝遵守 Robot协议 ！
作者：小蜗牛Snail丶
链接：https://www.jianshu.com/p/1b5d7d904b21"""
class ZwSpider(scrapy.Spider):
    name = 'zw'
    allowed_domains = ['cnki.net']
    start_urls = "https://kns.cnki.net/kns/request/SearchHandler.ashx"
    i = 1

    # 这里重写start_requests,改成发送post请求，在body的form-data表单中或者说chrome的headers中的form data中的就是post请求的参数
    # 这里我们通过postman插件或者说app模拟了这一个请求
    # 每个参数的含义等详情请看  ==》 https://blog.csdn.net/qq_37244001/article/details/85161349
    def start_requests(self):
        self.search_value = input("请输入您要检索的文章题目关键词：")
        # 生成时间戳
        self.t = int(time.time())
        # print(self.t, "============================")
        # 制作formdata表单
        formdata = {
            "NaviCode": "*",
            "ua": "1.21",
            "isinEn": "1",
            "PageName": "ASP.brief_result_aspx",
            "DbPrefix": "SCDB",
            "DbCatalog": "中国学术文献网络出版总库",
            "ConfigFile": "SCDB.xml",
            "db_opt": "CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD",
            "CKB_extension": "ZYW",
            "txt_1_sel": "SU$%=|",
            "txt_1_value1": str(self.search_value),
            "txt_1_relation": "#CNKI_AND",
            "txt_1_special1": "=",
            "his": "0",
            "__": str(self.t),
        }
        print(self.start_urls)
        # print("111111111111111111")
        # 递交form表单，发送post请求，从而得到我们的目标cookies
        # callback其实不是为了传递response，而是得到cookies之后，进行下一个页面也就是我们想要的总论文页面的请求，注意下一个页面的时间戳要和这个页面的一样，其他的值并没有改变
        yield scrapy.FormRequest(
            url=self.start_urls,
            formdata=formdata,
            callback=self.parse
        )

    # 时间戳随便设置，但前后的时间戳一定要相等
    # 请求总页面
    def parse(self, response):
        print("222222222222222222222222")
        url = f"https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&isinEn=1&dbPrefix=SCDB&" \
              f"dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&" \
              f"ConfigFile=SCDB.xml&research=off&t={self.t}&keyValue={self.search_value}&S=1&sorttype="

        # 凭借着start_parse得到的cookies，去请求我们想要检索的论文url列表
        yield scrapy.Request(
            url=url,
            callback=self.get_thesis_url
        )

                                                        # 这里注意一下，url
    # 提取检索出来的每一个论文的url
    def get_thesis_url(self, response):
        print(f"=============================>第{self.i}页<===================================")
        self.i += 1

        value_list = response.xpath("//tr/td/input/@value").extract()
        for value in value_list:
            # 得到拼装url需要的两个参数
            dbname = value.split("!")[0]
            filename = value.split("!")[1]
            print(filename)

            # 本来里面还要一个挺麻烦的参数dbcode=CJFD，这个应该是用来确定我们检索内容的分类，但仔细一想，
            # 这个参数在我们请求论文详情页的url时，并没有起到非常关键的定位作用，只是一个笼统的将论文分类的作用，
            # 所以我们尝试将其
            # url = f"https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFD&dbname={dbname}&filename={filename}"
            url = f"https://kns.cnki.net/KCMS/detail/detail.aspx?dbname={dbname}&filename={filename}"
            # 请求每一个论文的的url
            # time.sleep(random.random() * 3)  # 通过sleep的方式访问，防止被检测出来，把我们的ip封掉  ==>  这句写的很好
            yield scrapy.Request(
                url=url,
                callback=self.thesis_data
            )

        # 请求下一页
        next_url = "https://kns.cnki.net/kns/brief/brief.aspx" + response.xpath("//a[text()='下一页']/@href").extract_first()
        if self.i > 4:
            return
        print(next_url)
        yield scrapy.Request(
            url=next_url,
            callback=self.get_thesis_url
        )

    def thesis_data(self, response):
        item = dict()

        # 中英文的题目格式不太一样，所以要分别用不同的xpath来抓取
        item["title"] = response.xpath("//h2[@class='title']/text()").extract_first() \
            if response.xpath("//h2[@class='title']/text()").extract_first() is not None \
            else response.xpath("//h2[@class='titleE']/text()").extract_first()
        item["keywords"] = response.xpath("//label[text()='关键词：']/../a/text()").extract() \
            if len(response.xpath("//label[text()='关键词：']/../a/text()").extract())>0 \
            else response.xpath("//label[@id='catalog_KEYWORD']/../a/text()").extract()
        item["abstract"] = response.xpath("//span[@id='ChDivSummary']/text()").extract_first()
        print(item)
        pass


