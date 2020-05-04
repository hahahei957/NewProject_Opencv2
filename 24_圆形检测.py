import cv2 as cv
import numpy as np


# 这个检测圆的函数对噪点太敏感了
def detect_circle(image):
    # 边缘保留滤波
    dst = cv.pyrMeanShiftFiltering(image, 10, 100)       # sp和sr采用10和100的效果是最高的

    # dst = cv.bilateralFilter(image, 0, 80, 15)
    # dst = cv.GaussianBlur(image, (3, 3), 0)

    cimage = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

    "https://blog.csdn.net/zhazhiqiang/article/details/51096727  dp: 分辨率累加器，minDIST: 明显区分的两个不同圆之间的最小距离 "
    " minRadius=0, maxRadius=0即圆的半径范围取默认值         param1=50, param2=30：边缘阈值的上下限"
    "method貌似只能是cv.HOUGH_GRADIENT"
    circles = cv.HoughCircles(cimage, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))  # 将结果转换成整型

    for circle in circles[0, :]:  # 从0开始得到全部的圆？？？
        cv.circle(image, (circle[0], circle[1]), circle[2], (0, 0, 255), 2)

    cv.imshow("target", image)
    cv.imshow("cimage", cimage)
    cv.imshow("dst", dst)


src = cv.imread(r"D:\Users\acer\Desktop\zhaopian\1.jpg")
cv.imshow("hello world", src)
detect_circle(src)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()
