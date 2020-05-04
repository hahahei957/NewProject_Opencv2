import requests
import re

class DoubanSpyder:
    def __init__(self):
        self.url = "https://movie.douban.com/top250?start={}&filter="
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

    def get_url(self, page):
        return self.url.format(page)

    def get_html_str(self,url):
        return requests.get(url, headers=self.headers).content.decode()

    def get_target_message(self, html_message):
        return re.findall("img width=\"100\" alt=(.*?) src=", html_message)

    def save_film_name(self, taget_str_lists):
        with open("豆瓣top250.txt", "a",  encoding="utf-8") as f:
            print("_______________________换页______________________________")
            for taget_str in taget_str_lists:
                f.write(taget_str)
                f.write("\n")


    def run(self):
        page = 0
        while page<250:
            # 1.获得目标网址
            url = self.get_url(page)
            page += 25
            # 2.发送请求，获得相应
            html_message = self.get_html_str(url)
            # 3.提取目标内容
            taget_str_lists = self.get_target_message(html_message)
            # 4.保存
            self.save_film_name(taget_str_lists)

if __name__ == "__main__":
    douban_top_250 = DoubanSpyder()
    douban_top_250.run()