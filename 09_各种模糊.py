"""
模糊就是为了减小图像各个成员像素之间的差异

-->  https://www.cnblogs.com/invisible2/p/9177018.html
"""

import cv2 as cv
import numpy as np


# 标准盒式过滤器来平湖图像
def blur(scr):
    dst = cv.blur(scr, (1, 10))
    cv.imshow("blur_zongxiang", dst)
    dst_2 = cv.blur(scr, (5, 1))
    cv.imshow("blur_hengxiang", dst_2)


# 可以更好的去除椒盐噪点
def median_blur(src):
    dst = cv.medianBlur(src, 9)  # 注意这里的取值只能是奇数， 且这个均值模糊只考虑位置上的附近点的权重和中心点的权重一样
    cv.imshow("median_blur", dst)


# 自定义的模糊
def custom_blur_demo(src):
    # 矩阵中元素的类型必须是np.float32的
    kernel_01 = np.ones([5, 5], np.float32) / 25  # 总之矩阵中每个元素之和为1， 例如这里这个是5*5的矩阵，每个点的值为1/25，共25个点，所以和一共为1

    # ddepth的默认值为-1
    dst = cv.filter2D(src, ddepth=-1, kernel=kernel_01)

    # 可以使得图像锐化， 这个矩阵是一个特殊分布的特殊规则的矩阵
    """OpenCV滤波器内核Kernel   -->     https://blog.csdn.net/Bigat/article/details/80792865"""
    kernel_02 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)

    "当目标图像的所需深度(ddepth) = -1时，表示输出图像与原图像有相同的深度。"
    "Python-OpenCV中的filter2D()函数 --> 很好的文章 https://www.cnblogs.com/lfri/p/10599420.html"
    dst = cv.filter2D(src, ddepth=-1, kernel=kernel_02)
    cv.imshow("custom", dst)


src = cv.imread(r"example.png")

blur(src)
median_blur(src)
custom_blur_demo(src)
cv.imshow("hello world", src)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()
