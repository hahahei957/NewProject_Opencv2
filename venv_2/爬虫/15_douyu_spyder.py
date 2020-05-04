"""
爬取斗鱼所有主播的
request直接请求这个网址即可  -->  https://www.douyu.com/gapi/rkc/directory/2_1/1
"""
from selenium import webdriver
import time
from selenium.common import exceptions as ex

class DoubanSpyder:
    def __init__(self):
        pass

    def parse_url(self, start_url):
        driver = webdriver.Chrome()
        driver.get(start_url)
        return driver

    """这里本来想通过driver一起获取到页面信息，但一直报错，解决不了  element is not attached to the page document"""
    def get_content_list(self, driver):

        # 一定要注意先分好组


        li_list = driver.find_elements_by_xpath("//ul[@class='layout-Cover-list']/li")
        content_list = list()
        print(li_list)
        for li in li_list:
            item = dict()
            "由于斗鱼的页面可能存在过一会自动刷新一下数据的情况，导致我们的页面过一会就会被刷新一次"
            try:
                item["title"] = li.find_element_by_xpath(".//h3").get_attribute('title')
            except ex.StaleElementReferenceException:
                print("\n")
                time.sleep(1)
                print(111)
                item["title"] = li.find_element_by_xpath(".//h3").get_attribute('title')
            time.sleep(1)
            print(1)
            # item["span"] = li.find_element_by_xpath(".//div/a[1]/div[2]/span").text
            print(2)
            content_list.append(item)
            print(content_list)
        print(2)
        return content_list


    def save_mesg(self, content_list):
        print(content_list)

    def run(self, sort):
        # 获取start_url
        start_url = "https://www.douyu.com/g_{}".format(sort)
        # 发送请求，获取相应
        driver = self.parse_url(start_url)
        # 提取处理数据
        content_list = self.get_content_list(driver)
        # 保存
        self.save_mesg(content_list)
        i = 0
        while True:
            # 获取next_url
            """Python爬虫怎么获取下一页的URL和网页内容？   -->  等着好好查一查"""
            # 不知道为啥要加上time.sleep(2)，不加上的话就会报错：Unable to locate element
            # 我暂时认为，查询'下一页'按钮对应的url需要一些延迟，否则就会报错
            time.sleep(2)
            driver.find_element_by_xpath("//li[@title='下一页']/span").click()
            # 这个睡眠是用于等待下一个页面刷新完成
            time.sleep(2)
            # 提取处理数据
            content_list = self.get_content_list(driver)
            # 保存
            self.save_mesg(content_list)
            print("___________________________________________", i)
            i -= 1


if __name__ == "__main__":
    douban = DoubanSpyder()
    douban.run('LOL')