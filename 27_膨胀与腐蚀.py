"""
形态学操作
"""

import cv2 as cv
import numpy as np


"将白色区域腐蚀了"
"腐蚀就是用图像中的最小值替换矩阵中间的值，也可以理解为逻辑运算中的与运算"
def erode(image):
    print(image.shape)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    cv.imshow("binary", binary)

    # 得到结构元素， 支持矩形和结构较差的， 我们一般都选择MORPH_RECT矩形， ksize结构元素我们选为3*3
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dst = cv.erode(binary, kernel)
    cv.imshow("erode", dst)


"膨胀函数就是将矩阵中的最大值替代中心点的值， 也就是并运算"
def dilate(image):
    print(image.shape)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    cv.imshow("binary", binary)

    # 得到结构元素， 支持矩形和结构较差的， 我们一般都选择MORPH_RECT矩形， ksize结构元素我们选为3*3
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dst = cv.dilate(binary, kernel)                   # 就只有这个函数和腐蚀不一样，这个是膨胀函数
    cv.imshow("dilate", dst)


src = cv.imread(r"D:\Users\acer\Desktop\phtots\open_06.jfif")
cv.imshow("hello world", src)
erode(src)

"也可以对彩色图像进行膨胀和腐蚀运算"
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
dst = cv.erode(src, kernel)
cv.imshow("colorful page", dst)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()