"""
ellipsis-2">面对疫情，企业该怎么做？——特劳特伙伴公司与创业伙伴的共同实践</span>
"""
import requests
import re

url = "https://36kr.com/"
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36"}
r = requests.get(url, headers=headers)

# 获取响应字段
html_str = r.content.decode()
# 匹配出目标字段
lines = re.findall(r"ellipsis-2\">(.*?)</span>", html_str)
print("匹配字段成功")
# 保存
with open("36kr中的标题", "a", encoding="utf-8") as f:
    for line in lines:
        f.write(line)
        f.write("\n")
    print("生成文件成功")