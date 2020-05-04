"""
图像梯度可以把图像看成二维离散函数，图像梯度其实就是这个二维离散函数的求导：
图像梯度: G(x,y) = dx(i,j) + dy(i,j);
dx(i,j) = I(i+1,j) - I(i,j);
dy(i,j) = I(i,j+1) - I(i,j);
其中，I是图像像素的值(如：RGB值)，(i,j)为像素的坐标。
图像梯度一般也可以用中值差分：
dx(i,j) = [I(i+1,j) - I(i-1,j)]/2;
dy(i,j) = [I(i,j+1) - I(i,j-1)]/2;
图像边缘一般都是通过对图像进行梯度运算来实现的。
上面说的是简单的梯度定义，其实还有更多更复杂的梯度公式。
"""
import cv2 as cv
import numpy as np


"通过差分的二阶导数得到边界的图像  拉普拉斯算子"
def lapalian(image):
    dst = cv.Laplacian(image, cv.CV_32F)

    """opencv convertScaleAbs函数原理  范围内,计算绝对值,并将结果转换为8位。 -->  https://blog.csdn.net/qq_27278957/article/details/103642735"""
    lpls = cv.convertScaleAbs(dst)
    cv.imshow("lapalian", lpls)


"自制拉普拉斯算子，从而通过拉普拉斯实现像素梯度"
def custom_lapalian(image):
    # 卷积核各成员要素值之和为0时，则为拉普拉斯算子
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])

    "当目标图像的所需深度(ddepth) = -1时，表示输出图像与原图像有相同的深度 --> 很好的文章 https://www.cnblogs.com/lfri/p/10599420.html "
    dst = cv.filter2D(image, cv.CV_32F, kernel=kernel)

    """opencv convertScaleAbs函数原理  范围内,计算绝对值,并将结果转换为8位。 -->  https://blog.csdn.net/qq_27278957/article/details/103642735"""
    lpls = cv.convertScaleAbs(dst)
    cv.imshow("custom_lapalian", lpls)


"通过差分得到的一阶导数，在一阶导数去最大值的地方得到边界的图像 soble算子  --> https://blog.csdn.net/qq_29840153/article/details/90769385"
"sobel就是一阶微分？？？？？？"
def sobel_demo(image):
    """参数dx取1时，就是一阶差分,一阶差分具体定义-->https://baike.baidu.com/item/%E4%B8%80%E9%98%B6%E5%B7%AE%E5%88%86/3937421?fr=aladdin"""
    grad_x = cv.Sobel(image, cv.CV_32F, 1, 0)         # 配置x方向的sobel函数参量  -->  # 这个函数是求x方向的梯度
    grad_y = cv.Sobel(image, cv.CV_32F, 0, 1)         # 参数ddepth的范围不能太小， 要超过8U， 否则加和要超过256
    gradx = cv.convertScaleAbs(grad_x)
    grady = cv.convertScaleAbs(grad_y)

    cv.imshow("gradient-x", gradx)
    cv.imshow("gradient-y", grady)

    "addWeighted加权函数 --> addWeighted"
    gradxy = cv.addWeighted(gradx, 0.5, grady, 0.5, 0)
    cv.imshow("sobel-demo-xy", gradxy)


src = cv.imread(r"beautyful_view.jpg")
sobel_demo(src)
lapalian(src)
custom_lapalian(src)
cv.imshow("hello world", src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()