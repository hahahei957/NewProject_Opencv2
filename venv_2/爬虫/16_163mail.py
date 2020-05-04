from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://mail.163.com/")

driver.find_element_by_id("switchAccountLogin").click()

time.sleep(2)
"""用xpath通过这个句子（//iframe[@id='x-URS-iframe1581853343229.8936']）能够找到iframe，
但是里面的数字是个随机变量，所以我们可以通过xpath部分属性值的方法  -->  https://www.cnblogs.com/FBGG/p/10002705.html"""
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@id='x-URS-iframe1581853343229.8936']"))
time.sleep(1)

"""像这样带着auto-id的元素每次进入都会刷新, 造成元素无法重复定位最终导致一直报错Unable to locate element， 
我感觉包含长串数字的可能在每次登陆时这些都会刷新，  
解决方法  -->  https://www.cnblogs.com/FBGG/p/10002705.html"""
# driver.find_element_by_xpath("//*[@id='auto-id-1581851587473']").send_keys("1123322")
driver.find_element_by_xpath("//input[@name='email']").send_keys("1123322")

driver.find_element_by_xpath("//input[@name='password']").send_keys("1123322")

driver.find_element_by_xpath("//a[@id='dologin']").click()

