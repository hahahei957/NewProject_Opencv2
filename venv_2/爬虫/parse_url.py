import requests
from retrying import retry

headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36"}

@retry(stop_max_attempt_number=3)                     # retry装饰器会连续三次尝试重连，如果报错超过3次则会真的去报错
def __parse_url(url, proxies, method, post_data={}):
    print("_________尝试连接url__________")
    if method == "get":
        r = requests.get(url, headers=headers,timeout=5, proxies=proxies)
    else:
        r = requests.post(url, headers=headers,timeout=5, data=post_data,proxies=proxies)
    assert r.status_code == 200
    "　assert的作用是，如果其值为假（即为0），那么它先向stderr打印一条出错信息，然后通过调用 abort 来终止程序运行。请看下面的程序清单badptr.c："

    print("返回html_str成功")
    return r.content.decode()

def parse_url(url, method="get", data=None, proxies={}):
    try:
        html_str = __parse_url(url,proxies,method,data)     # 如果封装的函数不按照缺省参数的形式，这里就要按照顺序填入所需要的参数
    except:
        html_str = None
        print("失败")

    return html_str


if __name__ == "__main__":
    print(parse_url("http://www.baidu.com"))