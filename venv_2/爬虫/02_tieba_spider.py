import requests
import json

class TieBa:
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.url = "https://tieba.baidu.com/f?kw="+tieba_name+"&pn={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

    def get_url(self):
        # url_list = list()
        # for i in range(0,1000):
        #     url_list.append(self.url.format(i*50))
        # return url_list

        return [self.url.format(i*50) for i in range(1000)]

    def get_html(self, url):
        r = requests.get(url, "w",headers=self.headers)
        # 解压成utf-8的格式
        return r.content.decode()

    def save_html(self, file_page, content):
        "一定要注意这里是.html结尾的格式，否则就会报错"
        filename = self.tieba_name+"第{}页.txt".format(file_page)
        print(filename)
        # with open(filename, encoding="utf-8") as f:                   # 这里的encoding="utf-8"不是很懂
        #     f.write(content)
        f = open(filename, "w", encoding="utf-8")
        f.write(content)


    def run(self):
        # 获取所有网页的url
        url_list = self.get_url()
        # 遍历得到每一页的url,发送请求，获取响应，保存文件
        for i, url in enumerate(url_list):
            # 发送请求, 获取响应
            content = self.get_html(url)


            # print(json.loads(content))
            """可以这么理解，json.loads()函数是将字符串转化为字典
            json.dumps()函数是将字典转化为字符串
            而content的内容并不全是JSON字符串，开头前几句如<!DOCTYPE html>明显就不是JSON字符串"""


            # 保存
            self.save_html(i+1, content)

            # page_num = url_list.index(url) + 1  # 页码数   用这句得到页数也挺不错的


if __name__ == "__main__":
    tieba_spider = TieBa("李毅")
    tieba_spider.run()


