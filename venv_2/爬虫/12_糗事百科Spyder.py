import requests
from lxml import etree
import json

class QiushiSpyder:
    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}


    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(1, 14)]

    def parse_url(self, url):
        r = requests.get(url,headers=self.headers)
        return r.content.decode()

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@class='content-left']/div")    # 分组
        content_list = list()
        for div in div_list:

            "整个循环中看到的数据所在的网页的element框架样子我都保存在本路径下的 糗事百科.png中了"

            item = dict()
            item['content'] = div.xpath(".//div[@class='content']/span/text()")
            "得到的文段格式不对,每段文段的结尾都有回车符，而且我们取到的item[''content]是个列表，每个成员是一段字符串， 所以这里要通过循环调整一下格式"
            item['content'] = [i.replace("\n", "") for i in item['content']] if len(item['content'])>0 else None

            item['author-gender'] = div.xpath(".//div[contains(@class,'articleGender')/@class]")
            item['author-gender'] = [i.split(' ')[-1].replace('Icon', '') for i in item['author-gender']] if len(item['author-gender'])>0 else None

            item['author-age'] = div.xpath(".//div[contains(@class, 'articleGender')]/text()")
            item['author-age'] = item['author-age'][0] if len(item['author-age'])>0 else None

            item['content-img'] = div.xpath(".//div[@class='thumb']/a/img/@src")
            item['content-img'] = 'https://' + item['content-img'] if len(item['author-img'])>0 else None

            # 由于用户的头像分为匿名头像和个人头像，而这两者的地址格式是不一样的,但他们都属于div[@class='author clearfix']中不同的节点下的img/@src
            # 下面这个是一种寻址方式
            item['author-img'] = div.xpath(".//div[@class='author clearfix']//img/@src")
            item['author-img'] = 'https://' + item['author-img'][0] if len(item['author-img'])>0 else None

            item['stats_vote'] = div.xpath(".//span[@class='stats-vote']/i/text()")
            item['stats_vote'] = item['stats_vote'][0] if len(item['stats_vote'])>0 else None

            content_list.append(item)

        return content_list

    @staticmethod
    def save_content_list(self, content_list):
        # content_list中的每个成员都是一个大字典，所以在保存的时候我们可以用json.dumps将其转换成很好的格式
        with open("糗事百科.txt", a, encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))

    def run(self):
        # 得到url列表，因为我们要爬取的url地址规律明显，页码总数明确
        # 当我们要爬取的url地址规律不明显，总数不明确的时候，则要通过代码提取下一页
        url_list = self.get_url_list()

        for url in url_list:
            # 2.发送请求，获取相应
            """反反爬虫：添加随机User-agent、ip、cookies、或者使用session(当对方判断我们为爬虫时的解决方案)
            - 如果不登录
              - 准备刚开始能够成功请求对方网站的cookie，即接收对方网站设置在response的cookie
              - 下一次请求的时候，使用之前的列表中的cookie来请求
            - 如果登录
              - 准备多个账号
              - 使用程序获取每个账号的cookie
              - 之后请求登录之后才能访问的网站随机的选择cookie
            """
            html_str = self.parse_url(url)

            # 3.提取数据
            """具体看当前目录下的，爬虫代码解析_重点"""
            content_list = self.get_content_list(html_str)    # content_list中的每个成员都是一个大字典，所以在保存的时候我们可以用json.dumps将其转换成很好的格式
            # 4.保存
            self.save_content_list(content_list)
