import requests
from selenium import webdriver
import time
import json

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

    def format_cookies(self):
        self.cookies = self.driver.get_cookies()
        print(f"self.cookies:{self.cookies}")
        cookie_list = [i["name"] + ":" + i["value"] for i in self.cookies]
        cookMap = dict()
        for cookie in cookie_list:
            cookMap[cookie.split(":")[0]] = cookie.split(":")[1]
        print(f"cookMap:{cookMap}")
        return cookMap

    def set_head(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }

    # 这里的请求成功说明，在我们浏览器登陆的qq空间下线之前，我们用任意其他的浏览器携带这个的cookies都是可以登录的，虽然qq空间每次下线后cookies都会失效
    # 并且在这里我们发现requests模块和scrapy框架使用的cookies的格式都是相同的
    # 这个函数是用于测试请求头的设置用的
    def parse_url(self):
        get_url = "https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=3212367285&do=1&fupdate=1&clean=1&g_tk={}".format(self.g_tk)
        r = requests.get(url=get_url, headers=self.headers, cookies=self.cookMap)
        print("="*50)
        print(r.content.decode("utf-8"))
        return r.content.decode("utf-8")

    def get_content_list(self, content):

        #TODO 重点！！！ 我们要将response中的_Callback这几个字母删去，否则json无法将其处理成字典   !!!!!!!!!!!!!!!!!
        content = content.replace("_Callback(", "")
        content = content.replace(");", "")

        content_list = json.loads(content)["data"]["items_list"]
        print("2222222222222222222222222222")
        print(content_list)

        # 遍历字典得到的是键名
        # 注意：requests模块请求数据没法向scrapy框架那样，处理得到一组item就可以yield出去，这里是同时得到所有信息，
        # 所以我们先要将其分组，再添加到同一个列表中，这样就可以的到所有每一个item的信息了
        item_list =list()
        for data in content_list:
            item = dict()
            item["name"] = data["name"]
            item["uin"] = data["uin"]
            item_list.append(item)
        return item_list

    def save_data(self, item_list):
        with open("21_获取到的所有好友的qq号.txt", "a",encoding="utf-8") as f:
            print(item_list)
            for data in item_list:
                f.write(data["name"] + ":" + str(data["uin"]) + "\r\n")
            f.close()

    def run(self):
        # 将cookies转化成requset能使用的
        self.cookMap = dict()
        self.cookMap = self.format_cookies()
        # 设置request的请求头
        self.set_head()
        # 发送请求获取响应
        content = self.parse_url()
        print("--------------------11------------------")
        # print(content)
        # 数据处理
        item_list = self.get_content_list(content)
        # 数据存储
        self.save_data(item_list)

a = SpiderToQQ()
a.run()
