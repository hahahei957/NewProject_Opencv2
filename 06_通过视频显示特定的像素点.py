import cv2 as cv
import numpy as np


def extract_object():
    capture = cv.VideoCapture(0)
    while True:
        ret_boot, frame = capture.read()

        hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
        low_hsv = np.array([35, 43, 46])
        high_hsv = np.array([77, 255, 255])

        mask = cv.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

        # 我感觉这里取遮罩层也可以将两个图像进行相加或者相减的运算, 但这里会报错， 不知道为啥
        # 纠正：两个图像要想相加减，要求两个图像的矩阵大小、通道数量、图像类型都要相同，否则就会报错
        # mask_2 = cv.cvtColor(mask, cv.COLOR_HSV2BGR)
        # target = cv.subtract(frame, mask_2)
        target = cv.bitwise_and(frame, frame, mask=mask)

        cv.imshow("orginal", frame)
        cv.imshow("mask", mask)
        cv.imshow("target", target)

        cv.waitKey(50)


if __name__ == "__main__":
    extract_object()