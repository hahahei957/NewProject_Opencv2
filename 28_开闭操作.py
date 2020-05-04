"""
形态学操作
"""

import cv2 as cv
import numpy as np


"开操作 先腐蚀后膨胀，从而让图片上的白点消失而不改变图片整体的形状"
def open_demo(image):
    print(image.shape)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    cv.imshow("binary", binary)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 15))        # 也可以将15*15的矩阵该为1*15的矩阵，这样比较区间就是一个竖直的区间，从而实现只保留竖直的线段

    "开闭操作就只有这里的函数和膨胀腐蚀不一样"
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

    cv.imshow("open-result", binary)


"闭操作 先腐蚀后膨胀，从而让图片上的黑点小时而不改变土拍你整体的形状"
def close_demo(image):
    print(image.shape)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    cv.imshow("binary", binary)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 15))        # 也可以将15*15的矩阵该为1*15的矩阵，这样比较区间就是一个竖直的区间，从而实现只保留竖直的线段

    binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)         # 开操作 先腐蚀后膨胀

    cv.imshow("open-result", binary)


src = cv.imread(r"D:\Users\acer\Desktop\phtots\open_06.jfif")
cv.imshow("hello world", src)
open_demo(src)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()