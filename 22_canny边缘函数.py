"""
关于2个阈值参数：
低于阈值1的像素点会被认为不是边缘；
高于阈值2的像素点会被认为是边缘；
在阈值1和阈值2之间的像素点,若与第2步得到的边缘像素点相邻，则被认为是边缘，否则被认为不是边缘。

https://blog.csdn.net/MoreWindows/article/details/8239625

3.5 抑制孤立低阈值点

到目前为止，被划分为强边缘的像素点已经被确定为边缘，因为它们是从图
像中的真实边缘中提取出来的。然而，对于弱边缘像素，将会有一些争论，
因为这些像素可以从真实边缘提取也可以是因噪声或颜色变化引起的。为了
获得准确的结果，应该抑制由后者引起的弱边缘。通常，由真实边缘引起的
弱边缘像素将连接到强边缘像素，而噪声响应未连接。为了跟踪边缘连接，
通过查看弱边缘像素及其8个邻域像素，只要其中一个为强边缘像素，则该
弱边缘点就可以保留为真实的边缘。

https://www.cnblogs.com/techyan1990/p/7291771.html

非极大值抑制  -->  https://www.cnblogs.com/wangyaning/p/4236949.html
"""
import cv2 as cv
import numpy as np


"其实也就是图像的二值化"
def edge_demo(image):
    blurred = cv.GaussianBlur(image, (3, 3), 0)
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)

    # 求x方向的梯度 X Gradient
    xgrad = cv.Sobel(gray, cv.CV_16SC1, 1, 0)
    ygrad = cv.Sobel(gray, cv.CV_16SC1, 0, 1)

    # edge
    # edge_output = cv.Canny(xgrad, ygrad, 50, 150)       # 50和150分别是高低阈值       高低阈值常用1:3和1:2之间
    # edge_output = cv.Canny(xgrad, ygrad, 50, 150)
    edge_output = cv.Canny(gray, 50, 150)                 # 第一个参数表示输入图像，必须为单通道灰度图。

    cv.imshow("edge_output", edge_output)


src = cv.imread(r"beautyful_view.jpg")
edge_demo(src)
cv.imshow("hello world", src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()






