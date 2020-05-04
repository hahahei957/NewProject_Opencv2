import requests



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

"传入参数的形式"
params = {"wd":"haha"}

"最后面的问号可加可不加，不加的话，程序会自动帮你加上"
url_temp = "https://www.baidu.com/?"

"注意用requests调用post和get时的函数"
r = requests.get(url_temp, headers=headers, params=params)
print(r.status_code)       # 获取请求得到的网页的状态
print(r.request.url)       # 获取我们请求得到的网页网址


"下面这个更加简洁"
".format用起来和%s效果是一样的"
url_2 = "https://www.baidu.com/?wd={}".format("haha")
r = requests.get(url_2, headers=headers)
print(r.status_code)       # 获取请求得到的网页的状态
print(r.request.url)       # 获取我们请求得到的网页网址
