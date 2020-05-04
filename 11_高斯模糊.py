import cv2 as cv
import numpy as np


def clamp(pv):
    if pv > 255:
        return 255
    if pv < 0:
        return 0
    return pv


"""高斯模糊就是用的正太分布得到卷积核的, 正态分布又称高斯分布  -->  https://www.cnblogs.com/invisible2/p/9177018.html"""
# 下面这个是自己写的， 是高斯分布的大概原理， OpenCV中给了专门的高斯模糊函数dst = cv.GaussianBlur(src, (0, 0), 15)
def gaussian_noise(image):
    h, w, ch = image.shape
    for row in range(h):
        for line in range(w):
            """np.random.normal(0, 20, 3) 正态分布函数   -->  https://www.cnblogs.com/mandy-study/p/7871754.html"""
            s = np.random.normal(0, 5, 3)
            b = image[row, line, 0]  # 蓝色
            g = image[row, line, 1]  # 绿色
            r = image[row, line, 2]  # 红色

            image[row, line, 0] = clamp(b + s[0])          # 为每一个点的通道0加权
            image[row, line, 1] = clamp(g + s[1])          # 为每一个点的通道1加权
            image[row, line, 2] = clamp(r + s[2])          # 为每一个点的通道2加权
    cv.imshow("gaussian_noise", image)


image = cv.imread(r"beautyful_view.jpg")
cv.imshow("before", image)
gaussian_noise(image.copy())
dst = cv.GaussianBlur(image, (0, 0), 2)                  # --> opencv中的高斯模糊
cv.imshow("opencv_Guassian", dst)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()
print(np.random.normal(0, 20, 3))
