"""
3.直方图比较应用

（1）图像相似度比较

        如果我们有两张图像，并且这两张图像的直方图一样，或者有极高的相似度，那么在一定程度上，我们可以认为这两幅图是一样的，这就是直方图比较的应用之一。

（2）分析图像之间关系

        两张图像的直方图反映了该图像像素的分布情况，可以利用图像的直方图，来分析两张图像的关系。
————————————————
版权声明：本文为CSDN博主「水亦心」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/shuiyixin/article/details/80257822
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

"""通过bgr的直方图进行比较，将每个通道的256降维到16"""


def create_rgb_hist(image):
    h, w, ch = image.shape
    rgbHist = np.zeros([16 * 16 * 16, 1], np.float32)  # 创建一个16*16*16行1列的矩阵
    bsize = 256 / 16
    for row in range(h):
        for line in range(w):
            b = image[row, line, 0]  # 获取每一个通道的每一个点的像素值
            g = image[row, line, 1]
            r = image[row, line, 2]
            # np.int(b/bsize)*16*16相当于向右进位，如二进制中的011 => 110 是从3变成了6，相当于乘以权位
            index = np.int(b / bsize) * 16 * 16 + np.int(g / bsize) * 16 + np.int(r / bsize)
            rgbHist[np.int(index), 0] = rgbHist[np.int(index), 0] + 1  # 获取得到一个充满数据的16*16*16行1列的数组
    return rgbHist


def hist_compare(image1, image2):
    hist1 = create_rgb_hist(image1)
    hist2 = create_rgb_hist(image2)

    hist_1 = cv.calcHist([image1], [1], None, [256], [0, 256])
    hist_2 = cv.calcHist([image2], [1], None, [256], [0, 256])
    """       函数一共有三个参数，一个输入图像，一个输出图像，一个比较方法。比较方法的取值的情况
    为上面的四种方法，在OpenCV中，每个都有自己的名字：xiao相关性 ( CV_COMP_CORREL )；Chi-Squ
    are卡方 ( CV_COMP_CHISQR )；Intersection ( CV_COMP_INTERSECT )；Bhattacharyya 距离 巴氏距离( CV_COMP_BHATTACHARYYA )。
    """
    match1 = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
    match2 = cv.compareHist(hist1, hist2, cv.HISTCMP_CHISQR)
    match3 = cv.compareHist(hist1, hist2, cv.HISTCMP_BHATTACHARYYA)
    match4 = cv.compareHist(hist_1, hist_2, cv.HISTCMP_CORREL)
    print("相关性：%s  卡方：%s  巴氏距离：%s        %s " % (match1, match2, match3, match4))

image1 = cv.imread("lena.png")
image2 = cv.imread("lenanoise.png")
hist_compare(image1, image2)
cv.imshow("image1", image1)
cv.imshow("image2", image2)
cv.waitKey(0)



"""
从这里往后
"""