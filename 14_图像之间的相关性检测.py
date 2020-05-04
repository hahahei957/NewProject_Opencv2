import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


"""全局直方图均衡化"""
def equalHist_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    cv.imshow("gray", gray)
    """equalizeHist：直方图均衡化函数，能够有效增强对比度     -->   文章很好：https://blog.csdn.net/qq_18343569/article/details/48029245"""
    dst = cv.equalizeHist(gray)
    cv.imshow("equalizeHist", dst)

    "我感觉这样处理rgb的效果更好"
    b, g, r = cv.split(image)
    b_1 = cv.equalizeHist(b)
    g_1 = cv.equalizeHist(g)
    r_1 = cv.equalizeHist(r)
    dst = cv.merge([b_1, g_1, r_1])
    cv.imshow("san tong dao zhi fang tu jun heng hua", dst)

"""局部直方图均衡化"""
def clahe_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    clahe = cv.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    dst= clahe.apply(gray)
    cv.imshow("clahe_demo", dst)


src = cv.imread(r"beautyful_view.jpg")
equalHist_demo(src)
clahe_demo(src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()