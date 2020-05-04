"""
由于直方图常用于统计未处理过得原始数据
而这里给的是已经按照直方图的分布处理得到的数据，x轴的数据interval是直方图的形式，没有具体的数值，
所以对于这组数据，我们通过条形图的呈现出直方图的形式
"""

# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib import font_manager

interval = [0,5,10,15,20,25,30,35,40,45,60,90]
width = [5,5,5,5,5,5,5,5,5,15,30,60]
quantity = [836,2737,3723,3926,3596,1438,3273,642,824,613,215,47]

print(len(interval),len(width),len(quantity))

# 设置图形大小
plt.figure(figsize=(20,8),dpi=80)

plt.bar(interval, quantity, width=width)

# 设置x轴的刻度
temp_d = [5]+ width[:-1]
print("width[:-1]==>", width[:-1])                           # 切片 [:-1] 取不到最后一个元素
print("temp_d==>", temp_d)
_x = [i-temp_d[interval.index(i)]*0.5 for i in interval]     # _x对应的点是条形图在x坐标上的对称点,用interval的名字替代这些值
print("_x==>", _x)
print("interval==>", interval)
plt.xticks(_x, interval)

plt.grid(alpha=0.4)
plt.show()
