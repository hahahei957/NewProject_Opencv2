"""
先把框架搭出来(也就是先把图画出来)
再处理细节

# 这个是关于3月和10月的温度/时间图
"""
from matplotlib import pyplot as plt
import random
from matplotlib import font_manager

my_font = font_manager.FontProperties(fname=r"C:\Users\acer\AppData\Local\Microsoft\Windows\Fonts\4155_迷你简丫丫体.ttf")
y_3 = [11,17,16,11,12,11,12,6,6,7,8,9,12,15,14,17,18,21,16,17,20,14,15,15,15,19,21,22,22,22,23]
y_10 = [26,26,28,19,21,17,16,19,18,20,20,19,22,23,17,20,21,20,22,15,11,15,5,13,17,10,11,13,12,13,6]

x_3 = range(1, 32)
x_10 = range(51, 82)

plt.figure(figsize=(20,8), dpi=80)

# 和之前绘制折线图的唯一区别,使用scatter方法绘制散点图
plt.scatter(x_3, y_3, label="3月份")
plt.scatter(x_10, y_10, label="10月份")      # 相当于前面的plot

# 设置x轴的刻度
_x_tickes_3 = ["3月{}号".format(i) for i in x_3]
_x_tickes_10 = ["10月{}号".format(i-50) for i in x_10]
_sum_tickes = _x_tickes_3 + _x_tickes_10
sum_x_ = list(x_3) + list(x_10)
plt.xticks(sum_x_[::3], _sum_tickes[::3], fontproperties=my_font, color="#CD661D", rotation=45)
plt.yticks(range(min(list(y_3)+list(y_10))-5, max(list(y_3)+list(y_10))+5, 3), color="#CD661D")

# 是指图例
plt.legend(prop=my_font)

# 设置轴标签
plt.xlabel("时间", fontproperties=my_font)
plt.ylabel("温度", fontproperties=my_font)
plt.title("温度时间图", fontproperties=my_font)

# 绘制网格线
plt.grid(linestyle="--", alpha=0.3)

# 展示
plt.show()

