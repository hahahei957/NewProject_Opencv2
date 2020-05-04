"""
下载
当我们发现整个response的字段符合json语句，才可以用json.loads将句子变成字典
否则如果只有部分符合列表生成式则只能将局部符合json语句格式的句子(就是和字典长得差不多的字符串)取出来用loads转换成python中的字典
"""
import requests
import json


get_url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
r = requests.get(get_url, headers=headers)
movie_dict = json.loads(r.content.decode())
print(movie_dict)
print("\n")
"""下面这句多看看，挺好的， 通过列表生成式生成电影名字"""
print("-- name --\n", [movie_dict['subjects'][i]['title'] for i in range(len(movie_dict['subjects']))])
