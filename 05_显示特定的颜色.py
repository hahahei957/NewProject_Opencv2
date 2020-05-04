"""
要想将特定的颜色突显出来
RGB色彩空间很难达到，
我们需要将RGB转换成HSV这个色彩空间，
通过对转换成HSC后的图像进行处理，更加方便
RGB--HSV
RGB--YUV
这两个色彩空间之间的转换非常重要，
他们都与自己独特的定义像素值对应颜色的方式，
有利于我们对像素的处理
HSV中：H-->180  S-->255  V-->255

注意inRange函数的使用
"""


import cv2 as cv
import numpy as np


# 展示一些常用的色彩空间的图像的样子对比
def color_space_demo(image):
    cv.imshow("orginal_painting", image)

    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    cv.imshow("GRAY", gray)

    hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)
    cv.imshow("HSV", hsv)

    yuv = cv.cvtColor(image, cv.COLOR_RGB2YUV)
    cv.imshow("YUV", yuv)

    ycrcb = cv.cvtColor(image, cv.COLOR_RGB2YCR_CB)
    cv.imshow("YCRCB", ycrcb)


# 用装饰器弄上一个遮罩层试试
# 但这样好像无法实现，因为被装饰对象的内部资源无法传出来
# def shade(func):
#     def call_func(image):
#         print("开始装饰，哈哈哈")
#         func(image)
#
#         # 通过与或非中的与运算实现
#         cv.bitwise_and(image, mask)
#     return call_func


# 这里我们让他特定的捕捉黄色
# 用子弹的图片弄得挺失败的，不知道为啥
# 但用风景的弄得挺好的，难道是因为我调了hsv的值得原因吗
# @shade
def extract_object_photo(image):
    hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)
    # 查表可得
    # low_hsv = np.array([11, 43, 46])
    # high_hsv = np.array([34, 255, 255])
    low_hsv = np.array([70, 150, 50])
    high_hsv = np.array([120, 255, 255])
    """数组的常用函数
print np.arange(0,7,1,dtype=np.int16) # 0为起点，间隔为1时可缺省(引起歧义下不可缺省)
print np.ones((2,3,4),dtype=np.int16) # 2页，3行，4列，全1，指定数据类型
print np.zeros((2,3,4)) # 2页，3行，4列，全0
print np.empty((2,3)) #值取决于内存
print np.arange(0,10,2) # 起点为0，不超过10，步长为2
print np.linspace(-1,2,5) # 起点为-1，终点为2，取5个点
print np.random.randint(0,3,(2,3)) # 大于等于0，小于3，2行3列的随机整数

原文链接：https://blog.csdn.net/fu6543210/article/details/83240024
    """

    # inRange函数的使用
    mask = cv.inRange(hsv, low_hsv, high_hsv)

    # shade = cv.bitwise_and(image, image, mask=mask)               # 必须处理完图像以后，同意进行展现，因为这句函数写在mask展示完时，会一直报错

    print("_____________________________1")
    cv.imshow("orginal page", image)
    print("___________________________2")
    cv.imshow("target_page", mask)
    print("_______________________________3")

    # 主要是通过这个函数，仅显示出mask突显出来的图像， image并image还是image
    shade = cv.bitwise_and(image, image, mask=mask)  # 必须处理完图像以后，同意进行展现，因为这句函数写在mask展示完时，会一直报错
    cv.imshow("shade windows", shade)



scr_view = cv.imread("magic_cube.jfif")
# color_space_demo(scr_view)

scr_bullet = cv.imread("zidan1.jpg")
extract_object_photo(scr_view)

cv.waitKey(0)
cv.destroyAllWindows()