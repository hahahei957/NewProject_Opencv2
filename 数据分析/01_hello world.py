from matplotlib import pyplot as plt
import random

x = range(0, 20)
y = [random.randint(20, 35) for i in range(20)]     # 得到随机的

plt.figure(figsize=(20, 8), dpi=80)        # figsize是指定图片大小， dpi是指定每英寸有几个像素点

# 设置x轴的刻度
x_list = [i/2 for i in range(0, 350, 1)]
plt.xticks(x_list)

# 设置y轴刻度   --用法和xticks一样，只不过这里我们最好是将范围设置在上下限之间
plt.yticks(range(min(y), max(y)+1)[::2])

plt.plot(x, y)
plt.show()