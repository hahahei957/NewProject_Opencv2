import cv2 as cv
import numpy as np

"""
https://blog.csdn.net/baidu_37366272/article/details/79928038
阈值化操作——cv::threshold()与cv::adaptiveThreshold()详解
"""


def threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 第二个参数是阈值，也就是二值图像的临界值， 大于该值得为1小于该值的为0，从而实现图像二值化
    # 但是，当后面有|cv.THRESH_OTSU方法， 则我们此处设置的阈值将会失效， 转而采用|cv.THRESH_OTSU函数产生的阈值
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY|cv.THRESH_OTSU)
    print("threshold value : %s" % ret)
    cv.imshow("binary", binary)


"在处理文字的方面更好一些"
def adaption_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)  # block_size必为奇数
    cv.imshow("adaption_threshold", binary)
    cv.imwrite("adaption_threshold tu xiangde er zhi hua.png", binary)


"用自己求出来的均值作为阈值去二值化图像"
def custom_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    h, w = image.shape[:2]
    m = np.reshape(gray, [1, w*h])
    mean = m.sum()/(w*h)
    ret, binary = cv.threshold(gray, mean, 255, cv.THRESH_BINARY)
    print("made by myself-->custom_threshold", ret)
    cv.imshow("made by myself-->custom_threshold", binary)


src = cv.imread(r"target_magic_cube.jpg")
x, y = src.shape[:2]
src = cv.resize(src, (int(x/2), int(y/2)))
# threshold(src)
adaption_threshold(src)
# custom_threshold(src)
cv.imshow("hello world", src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()
