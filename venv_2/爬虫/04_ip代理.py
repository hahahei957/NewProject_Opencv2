import requests

# 这里面的http://47.75.32.210:1080加不加http://都可以
proxies = {"http":"http://47.75.32.210:1080"}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

"这里一开始我尝试连接百度，结果出错了， 我觉得应该是百度判断出了爬虫行为，所以我随便连接了一个网站"
r = requests.get("https://blog.csdn.net/scx2006114/article/details/81330002", proxies=proxies, headers=headers)

print(r.status_code)