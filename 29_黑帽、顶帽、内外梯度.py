"""
最后一个内外梯度的好好看看，挺有意思的，其他的都是一样的
"""

import cv2 as cv
import numpy as np


"对顶帽的操作, 我感觉对二值图像操作更好一些，这里只是说明用gray也可以"
def hat_gray_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))      # 得到结构要素  cv.MORPH_RECT表示我们选择的每小块矩阵是矩形的
    dst = cv.morphologyEx(gray, cv.MORPH_TOPHAT, kernel)             # 形态学操作函数，通过cv.MORPH_TOPHAT方法

    cimage = np.array(gray.shape, np.uint8)
    cimage = 120

    dst = cv.add(dst, cimage)
    cv.imshow("top_hat", dst)


"对黑帽的操作 "
def black_hat_binary(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dst = cv.morphologyEx(binary, cv.MORPH_BLACKHAT, kernel)              # 通过这个实现黑帽的操作
    cv.imshow("black_hat", dst)


"图像的梯度， 实现的结果感觉就是只保留图像中各个图形的边缘"
def hat_binary_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dst = cv.morphologyEx(binary, cv.MORPH_GRADIENT, kernel)               # 通过cv.MORPH_GRADIENT这个方法实现梯度的操作
    cv.imshow("tophat", dst)


"即膨胀的结果减去原图的结果，从而实现了只保留外部扩张的轮廓"
"即原图的结果减去腐蚀的结果，从而实现了只保留内部扩张的轮廓"
def gradient2_demo(image):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dm = cv.dilate(image, kernel)
    em = cv.erode(image, kernel)
    dst1 = cv.subtract(image, em) # internal gradient    # 内梯度
    dst2 = cv.subtract(dm, image) # external gradient    # 外梯度
    cv.imshow("internal", dst1)                         # 即原图的结果减去腐蚀的结果，从而实现了只保留内部扩张的轮廓
    cv.imshow("external", dst2)                         # 即腐蚀的结果减去原图的结果，从而实现了只保留外部扩张的轮廓


src = cv.imread(r"D:\Users\acer\Desktop\phtots\open_06.jfif")
cv.imshow("hello world", src)
gradient2_demo(src)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()
