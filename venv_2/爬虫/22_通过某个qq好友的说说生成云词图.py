import requests
from selenium import webdriver
import time
import json
import random

USERAGENT_LIST = [ "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)", "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)", "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0", "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5" ]

class SpiderToQQ:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://qzone.qq.com/")
        self.driver.switch_to.frame('login_frame')           #切换到输入账号密码的框架
        # self.driver.find_element_by_xpath("//*[@id='switcher_plogin']").click()
        self.driver.find_element_by_xpath("//a[text()='帐号密码登录']").click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath("//input[@id='u']").clear()     # 先清空里面的内容
        qq_num = '3212367285'   # qq号码
        self.driver.find_element_by_xpath("//input[@id='u']").send_keys(qq_num)
        self.driver.find_element_by_xpath("//input[@id='p']").clear()
        self.driver.find_element_by_xpath("//input[@id='p']").send_keys('gt123456')
        self.driver.find_element_by_xpath("//input[@id='login_button']").click()
        time.sleep(8)
        self.driver.get(f"https://user.qzone.qq.com/{qq_num}/myhome/friends/index")
        self.g_tk = self.driver.execute_script('return QZONE.FP.getACSRFToken()')               # 这句话好难找到的，最好的方法还是破解js加密的方式或者执行js
        print(self.g_tk)
        print("-----------------------")
        # self.driver.quit()
        self.count = 1

    def set_head(self):
        # 处理cookies
        self.cookies = self.driver.get_cookies()
        cookies_list = [i["name"] + ":" + i["value"] for i in self.cookies]
        self.cookMap = dict()
        for cookie in cookies_list:
            self.cookMap[cookie.split(":")[0]] = cookie.split(":")[1]
        # 处理请求头
        self.UserAgent = random.choice(USERAGENT_LIST)

    def parse_url(self, target_qq_num):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
        r = requests.get(url=f"https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={target_qq_num}&inCharset=utf-8&outCharset=utf-8&hostUin={target_qq_num}&notice=0&sort=0&pos={20*self.count}&num=20&code_version=1&format=jsonp&need_private_comment=1&g_tk={self.g_tk}",
                         headers=self.headers, cookies=self.cookMap)
        print("-------------------------------parse_url")
        print(f"r.content.decode:{r.content.decode()}")
        return r.content.decode()

    def get_content_list(self, content):
        content = content.replace("_Callback(", "")
        content = content.replace(");", "")
        print(f"content:{content}")
        content_list = json.loads(content)["msglist"]
        item_list = list()
        for blog in content_list:
            item = dict()
            item["createTime"] = blog["createTime"]
            item["content"] = blog["content"]
            item["commentlist"] = [i["createTime2"] + "--" + i["name"] + i["content"] for i in blog["commentlist"]]
            item_list.append(item)
        print("-------------------------------get_content_list")
        return item_list

    def save(self):
        pass

    def run(self, target_qq_num):
        # 设置请求头
        self.set_head()
        while True:
            # 发送请求获取响应
            content = self.parse_url(target_qq_num)
            self.count += 1
            # 数据处理
            item_list = self.get_content_list(content)
            # 存储数据
            print(item_list)
            self.save()
        # 请求
test = SpiderToQQ()
test.run(52030187)