"""
先把框架搭出来(也就是先把图画出来)
再处理细节
"""
from matplotlib import pyplot as plt
import random
from matplotlib import font_manager

# font = matplotlib.rc("font", family="Blackoak Std 黑体")
my_font = font_manager.FontProperties(fname=r"C:\Users\acer\AppData\Local\Microsoft\Windows\Fonts\4155_迷你简丫丫体.ttf")

x = range(0, 20)
y = [random.randint(20, 35) for i in range(20)]     # 得到随机的
y_2 = [random.randint(10, 40) for a in range(20)]     # 得到随机的

plt.figure(figsize=(20, 8), dpi=80)        # figsize是指定图片大小， dpi是指定每英寸有几个像素点

# 设置x轴的刻度为中文
_x_ticks = [i for i in range(0, 60)]
_x_ticks_lable = ["10点{}分".format(i) for i in range(60)]
plt.xticks(_x_ticks, _x_ticks_lable, rotation=45, fontproperties=my_font)

# 绘制网格
plt.grid(alpha=0.5)

plt.plot(x, y, label="气温",  color="#FFDEAD")
plt.plot(x, y_2, label="气温_2",  color="#98F5FF", linestyle="--")

# 添加图例                        # 图例的设置一定要在图画出来之后再设置
plt.legend(prop=my_font)

plt.show()