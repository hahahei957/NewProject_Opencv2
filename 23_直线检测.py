import cv2 as cv
import numpy as np


"""这个函数虽然是用于直线检测， 但不是很常用， 主要用于理解函数的处理过程"""
"函数cv.HoughLinesP比cv.HoughLines函数更常用也更加方便"
def line_dection(image):
    dst = cv.GaussianBlur(image, (3, 3), 0)
    gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

    gray2canny = cv.Canny(gray, 50, 150)

    lines = cv.HoughLines(gray2canny, 1, np.pi/180, 200)
    # 下面好像是对得到的每条线进行单独处理
    for line in lines:
        print(type(lines))
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0-1000*(-b))
        y2 = int(y0-1000*(a))
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv.imshow("image-lines", image)


"函数cv.HoughLinesP比cv.HoughLines函数更常用也更加方便"
def line_dection_possible(image):
    # dst = cv.GaussianBlur(image, (1, 1), 0)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray2canny = cv.Canny(gray, 50, 150)
    "minLineLength:控制线段最短长度， maxLineGap：控制线段中最长的间隔"
    "rho：累加器的距离分辨率，以像素为单位       theta：累加器的角度分辨率，以弧度表示"
    "分辨率应该就是间隔多少距离去检测一个点"
    lines = cv.HoughLinesP(gray2canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=50)
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv.line(gray2canny, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv.imshow("target", image)
    cv.imshow("gray2canny", gray2canny)
    cv.imwrite("target_magic_cube.jpg", image)


src = cv.imread(r"magic_cube_2.jfif")
cv.imshow("hello world", src)
line_dection_possible(src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()