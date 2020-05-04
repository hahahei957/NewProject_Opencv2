import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def back_projection_demo():
    sample = cv.imread("soccer_local.png")
    target = cv.imread("soccer_target.png")
    sample_hsv = cv.cvtColor(sample, cv.COLOR_RGB2HSV)
    target_hsv = cv.cvtColor(target, cv.COLOR_RGB2HSV)

    cv.imshow("sample", sample)
    cv.imshow("target", target)

    # 通过hsv中的两个通道的值来生成两个直方图，每个直方图有32个分布区域，通过两个通道来确定图像所在的位置比较合适
    sampleHist = cv.calcHist([sample_hsv], [0, 1], None, [32, 32], [0, 180, 0, 255])  # 第13个历程也用到了这个函数， 两者可以对比区分一下
    print(sampleHist, "-------------->sampleHist")
    cv.imshow("sampleHist1", sampleHist)

    """cv.normalize: 归一化数据。该函数分为范围归一化与数据值归一化。   -->  https://blog.csdn.net/cosmispower/article/details/64457406
    但是，这句话有没有运行结果都一样（因为感觉原图就进行了这样的处理）"""
    # TODO:111111111111111111111111
    cv.normalize(sampleHist, sample_hsv, 0, 255, cv.NORM_MINMAX)
    cv.imshow("sampleHist2", sampleHist)

    """两个通道可以近似确定图像所在的位置， 如果通过三个通道去确定， 则只有一模一样的区域是几乎不存在的， 所以只用两个通道去近似选则区域是最合适的
    calcBackProject()：  -->  https://blog.csdn.net/keith_bb/article/details/70154219
    """
    # 重点：反向投影在这里的应用是，我们向统计sampleHist的直方图，再通过直方图每个区段含有的像素数量，反向到目标图像，
    # 根据目标图像每个像素点在sampleHist直方图的哪一个像素范围内，将sampleHist直方图统计出来的那个区域的像素数量来替代目标图像这个像素点的值，
    # 以此类推，目标图像的每一个点进行如上处理后，得到一个全新的矩阵，这个矩阵的每一个像素点的值将变成sample直方图某一分区内含盖该像素值出现的数量
    # 再将该矩阵进行展示，哪个点越亮，说明sample图像很有可能在target的该点分布，
    # 我感觉（但这个解释也不太对）由于我们通过normalize将直方图纵坐标均匀分到了0-255，得到纵坐标数量最多值将会被替代为255，
    # 具体解释看这个地址  ==》  https://blog.csdn.net/michaelhan3/article/details/73550643?depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-3&utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-3
    dst = cv.calcBackProject([target_hsv], [0, 1], sampleHist, [0, 180, 0, 255], 1)
    cv.imshow("dst", dst)


def hist2d_demo(image):
    hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)
    hist = cv.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    plt.imshow(hist, interpolation="nearest")     # 原理：plt.imshow()函数负责对图像进行处理，并显示其格式，而plt.show()则是将plt.imshow()处理后的函数显示出来。
    plt.title("2D Histogram")
    plt.show()


image = cv.imread("soccer_target.png")
back_projection_demo()
hist2d_demo(image)
cv.waitKey(0)



