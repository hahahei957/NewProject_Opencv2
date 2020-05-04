import requests
import os
from lxml import etree
import re
import cv2 as cv

class GloryOfKings:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safar}i/537.36"}

    def parse_url(self, url, flag=False):
        r = requests.get(url=url, headers=self.headers)

        # 如果flag是True是用来解析图片格式的响应的，直接以二进制的形式返回数据即可，因为响应的到的二进制图片用.decode()的时候会报错
        if flag:
            return r.content
        # 使用return r.content.decode(）解析html时候出现如下错误：
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcd in position 278: invalid continuation byte
        # 出现上述错误，绝大多数原因是这个响应不是utf-8编码的，例如可能是gbk编码的，所以我们使用utf-8解码会报错，尝试改成gbk等解码方式试试，就可以解决问题
        return r.content.decode("gbk")                      # 这里要改成gbk，因为有些文字超出了utf-8的范畴，


    """etree的使用"""
    def get_heros_list(self, content):
        # 把网页传给etree，从而可以用xpath来进行检索
        html = etree.HTML(content)
        heros_url_list = html.xpath("//ul[@class='herolist clearfix']/li/a/@href")
        heros_url_list = ["https://pvp.qq.com/web201605/"+i for i in heros_url_list]
        return heros_url_list
        # heros_name_list = html.xpath("//ul[@class='herolist clearfix']/li/a/text()")
        # return heros_name_list,heros_url_list

    def get_skins_num(self,content):
        html = etree.HTML(content)
        img_source_list = html.xpath("//ul[@class='pic-pf-list pic-pf-list3']/@data-imgname")[0]
        # print(img_source_list)
        n = img_source_list.count("|")+1             # 统计这个|字符出现的次数，从而得到某个英雄皮肤的数量，本来想用xpath提取的，但他的xpath关于皮肤的不仅与element中的不一样，而且还被注释掉了
        print(n)
        name = html.xpath("//div/h2/text()")[0]
        return name,n

    def run(self):
        # 发送请求获取王者荣耀url列表
        start_url = "https://pvp.qq.com/web201605/herolist.shtml"
        heros_content = self.parse_url(start_url)
        # 获取所有英雄列表
        # print(str(heros_content))
        heros_url_list = self.get_heros_list(heros_content)
        # print(heros_url_list)
        # 循环对每个英雄挨个请求
        for heros_url in heros_url_list:
            # 请求英雄详情页并获取响应
            content = self.parse_url(heros_url)
            # print(content)
            # 提取英雄名字和皮肤数量
            name, n = self.get_skins_num(content)
            # 循环请求每一个比附，并保存
            # hero_id = re.findall("(\d{3}).shtml", heros_url)[0]               # 这个得到的是列表类型，一定要记得转换
            hero_id = re.findall("(\d{3}).shtml", heros_url)[0]               # 这个得到的是列表类型，一定要记得转换

            print(n)
            for i in range(n):  # 一个英雄皮肤的数量肯定少于10
                img_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_id}/{hero_id}-bigskin-{i+1}.jpg"

                # 通过flag=True,我们直接将图片用二进制的形式读取出来，具体看parse_url函数中的注解
                img_source = self.parse_url(img_url,flag=True)
                print(img_source)
                save_file = name+"-"+str(i+1)+".jpg"

                # 这句中的每一个\都要再添加一个\消除其的作用
                save_file = "D:\\Users\\acer\Desktop\zhaopian\王者荣耀1\\"+save_file
                print(save_file)

                # 可以通过二进制直接保存图片
                with open(save_file, "wb") as f:
                    f.write(img_source)
                    f.close()
                # cv.imwrite(save_file,img=img_source)
                print(name,"--",i+1,"--","保存成功")

act = GloryOfKings()
act.run()