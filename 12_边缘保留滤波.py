import cv2 as cv
import numpy as np


"""边缘保留滤波是二维高斯分布（前面的高斯分布好像也是二维的， 但前面的二维是拆成两个一维的，都是是关于位置的）
这里边缘保留滤波中的二维高斯中的两个维度，分别对应考虑了像素点之间的位置差异加权和颜色差异加权"""
def bilateral(image):
    """https://blog.csdn.net/duwangthefirst/article/details/79971369"""
    "也就是在颜色相差不大的一片很大的区域内进行模糊"
    dst = cv.bilateralFilter(image, 0, 80, 15)             # 这个函数运行时间慢
    cv.imshow("bilateralFilter", dst)


"""效果不好， 有点像油画的感觉"""
"但是这个函数可以将图像内部信息做最大程度的模糊， 最大程度保留边缘"

"""这个函数严格来说并不是图像的分割，而是图像在色彩层面的平滑滤波，它可以中和色彩分布相近的颜色，平滑色彩细节
，侵蚀掉面积较小的颜色区域，所以在Opencv中它的后缀是滤波“Filter”，而不是分割“segment”。先列一下这个函数，再说一下它“分割”彩色图像的实现过程。"""
"https://blog.csdn.net/dcrmg/article/details/52705087"
def mean_shift_filtering(image):
    dst = cv.pyrMeanShiftFiltering(image, 10, 50)
    cv.imshow("MeanShiftFiltering", dst)


src = cv.imread(r"example.png")
cv.imshow("orignal", src)
bilateral(src)
mean_shift_filtering(src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()
