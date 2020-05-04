"""from: zh
to: en
query: 你好
transtype: realtime
simple_means_flag: 3
sign: 232427.485594
token: 365f655442425a8e3986f1c0ba6f9841"""

"""from: zh
to: en
query: 帅哥
transtype: realtime
simple_means_flag: 3
sign: 81401.384712
token: 365f655442425a8e3986f1c0ba6f9841"""

"""
Get和post的区别是什么
   1. Get是不安全的，因为在传输过程，数据被放在请求的URL中；Post的所有操作对用户来说都是不可见的。
   2. Get传送的数据量较小，这主要是因为受URL长度限制；Post传送的数据量较大，一般被默认为不受限制。
   3. Get限制Form表单的数据集的值必须为ASCII字符；而Post支持整个ISO10646字符集。
   4. Get执行效率却比Post方法好。Get是form提交的默认方法。 收起 
    https://www.cnblogs.com/logsharing/p/8448446.html
    """

# 由于我们写的是POST类型的数据所以需要穿参数给服务器
import requests
import json
import sys


query = sys.argv[1]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

# query = "你好"

post_data = {
"from": "zh",
"to": "en",
"query": query,
"transtype": "realtime",
"simple_means_flag": "3"
}

post_url = "https://fanyi.baidu.com/v2transapi"

r = requests.post(post_url, data=post_data, headers=headers)

print(r.content.decode())    # .decode()默认是以utf-8的形式
print(r.status_code)
dict_ret = json.loads(r.content.decode())          # 将json文件中的字符串转换为字典
ret = dict_ret["trans"][0]["dst"]
print("result is :",ret)

"由于百度翻译的post中有未知参量，手机和电脑版都有，导致程序无法正常运行"

