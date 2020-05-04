"""
在python中，只有函数才是Callable（可Call的对象才是Callable）。但是tuple是一个数据类型，当然是不能Call（翻译成：使唤，hhh可能会比较容易理解）
"""

import cv2 as cv
import numpy as np


def negation_pixels(image):
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    print("width: %s    height: %s    channels: %s    " % (width, height, channels))

    # 遍历每一个像素点的每一个通道，使他们的像素值取反
    for row in range(height):
        for col in range(width):
            for c in range(channels):
                pv = image[row, col, c]  # pv是image对象在第row行，第col列，第c通道的像素值
                image[row, col, c] = 255 - pv  # 像素值取反

    cv.imshow("negation pixels_1", image)


scr = cv.imread(r"beautyful_view.jpg")
cv.imshow("before", scr)
negation_pixels(scr)
cv.bitwise_not(scr)
cv.imshow("negation pixels_2", scr)
cv.waitKey(0)
cv.destroyAllWindows()