"""
目标：输入想要获取的网址的url即可得到对应网址的弹幕

API：
1. 一个提供特定功能的软件

2. 整个服务器、整个应用或一款应用的很小一部分

从本质上来说，任何能从自身环境中分离出来的软件都可以成为API中的“A”，且很可能它本身也是某种API。
就这么说吧，你在代码中使用的是第三方库。一旦该库与你的代码整合在了一起，那么这个库也就成为了整
体应用的一部分。作为软件中特殊的一部分，库很有可能也拥有一个API，使其与剩余代码进行交互。
"""
import requests
import re
from lxml import etree

class BlibliSpyder:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36"}
        self.url = "https://www.bilibili.com/video/av87996856?spm_id_from=333.851.b_7265706f7274466972737432.5"

    def get_url(self):
        # """//*[@id='bofqi']/div/div[2]/video/source/@src"""
        # "//div[@id='page']//div[@class='player-box']//source/@src"
        # "上面那两个匹配到的东西是一样的"
        html_str = self.parse_url(self.url)
        print("###################")

        "用正则表达式的时候一定要用正则表达式在线测试的工具测试一下"
        "response返回的内容，就是我们得到的html_str, 两者是一样的"
        target = re.findall("comment: '//comment\.bilibili\.com/' \+ (\d*?) \+ '\.xml'", html_str) if len(re.findall(r"comment: '//comment\.bilibili\.com/' \+ (\d*?) \+ '\.xml'", html_str))>0 else None
        print(target)
        # 这里可能会报错
        conment_url = 'https://comment.bilibili.com/' + target[0] + '.xml'
        return conment_url

    def parse_url(self, url):

        """headers一定要带上， 否则页面给你返回的html很可能会少参数，在这个程序中，就少给了好多scribe文件"""
        r = requests.get(url, headers= self.headers)
        return r.content.decode()

    def get_content_list(self, html_str):
        content_list = re.findall(">(.*?)</d><d p=", html_str)
        return content_list

    def save_mesg(self, content_list):
        with open("blibli弹幕.txt", "a", encoding='utf-8') as f:
            for content in content_list:
                f.write(content)
                f.write("\n")
            f.close()
        print("保存成功")

    def run(self):
        # 1.输入视频网址，获取视频弹幕的网址
        conment_url = self.get_url()
        pass
        # 2.发送请求，获取相应
        html_str = self.parse_url(conment_url)
        # 3.分析获得目标数据
        print(html_str)
        content_list = self.get_content_list(html_str)
        # 4.保存
        self.save_mesg(content_list)


if __name__=="__main__":
    blibli = BlibliSpyder()
    blibli.run()

""" script脚本中的text文档符合JSON语句，我们可以通过json.load将其转换为字典类型的数据来进行提取

   <script type="application/ld+json">
        
    {
        "@context": "https://zhanzhang.baidu.com/contexts/cambrian.jsonld",
        "@id": "http://m.bilibili.com/video/av88068475.html",
        "appid": "1580859622074471",
        "title": "对王之王你大爷",
        "images": [
            "https://i1.hdslb.com/bfs/archive/aa0d305e2595b775500d63e1cf0bdc97b7c463b2.jpg@400w_300h.jpg"
            ],
        "description": "电脑上已经没什么软件能用了，凑合看吧。 。 。 。 。 。 。 。 。 本视频所有收益将全部捐出。",
        "pubDate": "2020-02-10T22:45:44"
    }
"""