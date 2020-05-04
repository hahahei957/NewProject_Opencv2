# from selenium import webdriver
# import time
#
#
# browser = webdriver.Chrome()
# browser.get('https://mail.qq.com/cgi-bin/loginpage')
# browser.switch_to.frame('login_frame') #找到邮箱账号登录框对应的iframe
# browser.find_element_by_id('u').send_keys('111') #找到邮箱账号输入框
# time.sleep(3)
# browser.find_element_by_id('p').send_keys('111') #找到密码输入框
# time.sleep(3)
# browser.find_element_by_class_name('login_button').click() #点击登陆按钮


# from selenium import webdriver
#
# def open_chrome():
#     chrome_drivers = webdriver.Chrome()
#     return chrome_drivers
#
# def login(search_form):
#     url = "https://mail.qq.com/"
#     search_form.get(url)
#     frame = search_form.find_element_by_id('login_frame')
#     search_form.switch_to.frame(frame)
#
#     username = search_form.find_element_by_id("u")
#
#     username.send_keys("222")
#
#     password = search_form.find_element_by_id("p")
#
#     password.send_keys("3333")
#
#     # submitclass = search_form.find_element_by_class_name("submit")
#     search_form.find_element_by_id("login_button").click()
#     print('Finished')
#
# if __name__ == '__main__':
#     drivers = open_chrome()
#     login(drivers)

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://mail.qq.com/")

driver.switch_to.frame("login_frame")

driver.find_element_by_xpath("//*[@id='u']").send_keys("111111111")
driver.find_element_by_xpath("//*[@id='p']").send_keys("1222222222")


