from selenium import webdriver
import time
# 实例化一个窗口
driver = webdriver.Chrome()

# 最大化窗口
driver.maximize_window()

# 发送请求
driver.get("http://www.baidu.com")

# 在百度中搜索qq邮箱并进入登陆界面
driver.find_element_by_id("kw").send_keys('qq邮箱')
driver.find_element_by_id('su').click()
time.sleep(2)

driver.find_element_by_xpath("//*[@id='1']/h3/a/em").click()
# 输入账号和密码登录
time.sleep(2)


"当页面切换时，句柄也要切换到新的界面 (通俗说：就是我们打开了一个新的界面，这个不同于在同一界面上请求新的页面，如点击下一页的操作只会在原界面上请求下一页)       -->      https://www.cnblogs.com/Test-road-me/p/4890920.html"
print(1)
driver.switch_to.window(driver.window_handles[1])
# driver.switch_to.default_content()	#回到主框架

# driver.switch_to.frame('login_frame')
print(2)

driver.switch_to.frame('login_frame')
time.sleep(1)
driver.find_element_by_xpath("//*[@id='u']").send_keys('3212367285')
driver.find_element_by_id('p').send_keys('gt123456')

driver.find_element_by_id('login_button').click()




"""# 进行页面截图
driver.save_screenshot("./baidu.png")

# 元素定位方法
"这句很重要"
driver.find_element_by_id('kw').send_keys("chromedriver安装")
driver.find_element_by_id('su').click()
time.sleep(2)

# 这个就是模仿我们点击我们通过xpath定位到的位置
driver.find_element_by_xpath("//div[@id='content_left']/div[@id='1']//a").click()
"""

# time.sleep(3)
# driver.quit()