import requests
import json


# post_url = "https://fanyi.baidu.com/langdetect"
#
# "一定注意headers这个字典"
# headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36"}
# post_data = {"query":"你好"}
# post_r = requests.post(post_url, data=post_data, headers=headers)
#
# "显示返回的状态"
# print(post_r.status_code)
#
# print(json.loads(post_r.content.decode())["lan"])



class Auto:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36"}

    def get_url(self, string):
        post_url = "https://fanyi.baidu.com/langdetect"
        post_data1 = {"query":string}
        print(post_data1)
        r1 = requests.post(post_url, data=post_data1, headers=self.headers)
        lan = json.loads(r1.content.decode())['lan']
        print(111111111111)
        print(lan)
        print(2222222222222222)
        post_data2 = {"from": "zh",
        "to": "en",
        "query": string,
        "transtype": "realtime",
        "simple_means_flag": 3,
        "sign": 232427.485594,
        "token": "f18a488a50b0179ee7c1c197f5aae6e8"
        }           if lan=='zh' else \
        {
            "from": "en",
            "to": "zh",
            "query": string,
            "transtype": "realtime",
            "simple_means_flag": 3,
            "sign": 232427.485594,
            "token": "f18a488a50b0179ee7c1c197f5aae6e8"
        }

        r2 = requests.post("https://fanyi.baidu.com/v2transapi?", headers=self.headers, data=post_data2)

        return r2.content.decode()

    def run(self):
        # 1.得到url
        pass
        string = input("请输入想要翻译的内容")
        # 2.发送请求、获取响应
        html_str = self.get_url(string)
        answer = html_str
        print(answer)
        # 3.保存

if __name__ == "__main__":
    trans = Auto()
    trans.run()