import zlib
import requests

# with open(r"E:\chrome下载的东西\14774604600_300_1 (4).z", "rb") as f:
#     res = f.read()
#     f.close()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
url = "https://cmts.iqiyi.com/bullet/46/00/14774604600_300_1.z"
r = requests.get(url, headers=headers)                  # 返回的是一个压缩包，但这里一样可以接收
res = r.content

zarray = bytearray(res)                                  # 我感觉就是将二进制内容的res转换成bytearray，也就是可变的字节序列，但对结果并没有啥影响

# zlib.decompress(zarray, 15+32) 15+32 这个参数 ==> 增大缓冲区，winsize默认是15
# xml=zlib.decompress(zarray, 15+32).decode('utf-8')
xml=zlib.decompress(res, 15+32).decode('utf-8')
print(xml)