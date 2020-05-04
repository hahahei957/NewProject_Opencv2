import requests
import json

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}

r = requests.get("https://careers.tencent.com/tencentcareer/api/post/Query?&pageIndex=1&pageSize=10", headers=headers)

print(r.content.decode("utf-8"))
content_dict = json.loads(r.content.decode("utf-8"))

temp_postion_list = content_dict["Data"]["Posts"]

item = dict()
item["name"] = [i["RecruitPostName"] for i in temp_postion_list]
print(item)