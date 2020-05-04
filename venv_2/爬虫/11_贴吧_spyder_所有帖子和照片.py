import requests
from lxml import etree
import json


class TiebaSpyder:
    def __init__(self, tieba_name):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
        # self.url = "https://tieba.baidu.com/f?kw=" + tieba_name + "&pn={}"
        self.url = "https://tieba.baidu.com/f?ie=utf-8&kw=%E6%9D%8E%E6%AF%85&fr=search"
        self.part_url = "https://tieba.baidu.com/"
        self.tieba_name = tieba_name

    def get_url(self, page):
        return self.url.format(20*page)

    def parse_url_str(self, url):
        r = requests.get(url)
        # print(r.content.decode())
        print("_"*50)
        return r.content.decode()

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        """加上encoding="utf-8"之后就可以正常显示中文了"""
        print(etree.tostring(html_str, encoding="utf-8").decode('utf-8'))
        # ti_title_list = html.xpath("//a[@class='j_common ti_item ']/div/span/text()")
        # ti_utl = "https://tieba.baidu.com/"

        div_list = html.xpath("//div[@contains, 'i']")
        content_list = list()
        for div in div_list:
            item = dict()
            item["title"] = div.xpath("./a/text()")[0] if len(div.xpath)>0 else None
            item["href"] = self.part_url + div.xpath("./a/@href")[0] if len(div.xpath)>0 else None

            item["img_list"] = self.img_list(item[href], total_img_list=[])
            item["img_list"] = div.xpath()[0] if len(div.xpath)>0 else None

            "将得到的图片链接处理一下，因为我们拿到的图片是在百度贴吧中的格式，所以图片带有很多格式，我们需要提取出原图的链接，也就是src=...后面的内容"
            "requests.utils.unquote(i)这个函数是实现对其的解码"
            item["img_list"] = [requests.utils.unquote(i).split('src=')[-1] for i in item["img_list"]]

            content_list.append(item)
        next_url = self.part_url + html.xpath["//a[text='下一页']/@href"][0] if len(html.xpath["//a[text='下一页']/@href"])>0 else None
        return content_list,next_url

    def img_list(self, detail_url, total_img_list):
        "由于评论可能分为好多页，要弄到所有页的图片"
        # 这句话是我自己添加的，因为当传入的网址为空，没有这句话可能就为空
        if detail_url == None:
            return None
        # 获取详情页的链接
        next_url = detail_url
        # 发送请求，获取响应
        html_str = self.parse_url_str(next_url)
        # 提取关于图片链接的信息
        html = etree.HTML(html_str)
        img = html.xpath()
        total_img_list.append(img)

        # 通过递归实现循环
        if len(html.xpath("//a[text()='下一页']"))>0:
            next_url = html.xpath("//a[text()='下一页']/@href")
            return self.img_list(next_url, total_img_list)
        # 保存
        return total_img_list

    def save_mesg(self, content_list):
        with open(self.tieba_name+'.txt', a, encoding='utf-8') as f:
            for content in content_list:

                # 因为每个content成员都是字典， 所以我们可以通过json.dumps将其转换为json语句，还好看一些，并且还可以使用
                "中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False："
                f.write(json.dumps(content,ensure_ascii=False,indent=2))
                f.write("\n")
        print("保存成功")

    def run(self):
        n = 0
        # 1.获取起始url
        next_url = self.get_url(n)
        while next_url is not None:
            # 2.发送请求，获取响应
            html_str = self.parse_url_str(url)
            html_2xpath = etree.HTML(text=html_str)
            # 3.解析数据的到想要的数据,并得到帖子内所有回复的图片
            "这里我们不用正则匹配数据了， 而是改用xml的xpath匹配大的数据"
            content_list, next_url = self.get_content_list(html_str)
            # 4.数据存储


if __name__ == "__main__":
    ti_liyi = TiebaSpyder("李毅")
    ti_liyi.run()

