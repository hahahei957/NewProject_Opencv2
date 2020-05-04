"""
直方图是图像中像素强度分布的图形表达方式.
它统计了每一个强度值所具有的像素个数.
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def plot_demo(image):
    """image.ravel()  -->  numpy中的ravel()、flatten()、squeeze()都有将多维数组转换为一维数组的功能，区别：
     https://blog.csdn.net/weixin_38632246/article/details/99121202
     https://blog.csdn.net/mosesRen/article/details/80275039"""
    """plt.hist()  -->  x对应的是所有的数据， 他们都会被填入对应的bins， bins是柱子的数量 ，range是x轴上的范围， 柱子在这个范围内均匀分布"""
    # plt.hist(image.ravel(), 256, [0, 256])
    plt.hist(image[:, :, 0].ravel(), 256, [0, 256])       # 这句话呈现的是处理blue这一个通道所对应的图像
    plt.show("直方图")

def image_hist(image):
    color = ('blue', 'green', 'red')
    for i, color in enumerate(color):
        # 第四个参数是histSize，表示这个直方图分成多少份（即多少个直方柱）。第二个例子将绘出直方图，到时候会清楚一点。
        # 最后是两个可选参数，由于直方图作为函数结果返回了，所以第六个hist就没有意义了（待确定） 最后一个accumulate是一个布尔值，用来表示直方图是否叠加。
        """https://www.jianshu.com/p/bd12c4273d7d"""
        hist = cv.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])        # 限定图像x轴方向的范围到最大值256就停下
    plt.show()


src = cv.imread(r"beautyful_view.jpg")
plot_demo(src)
image_hist(src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()