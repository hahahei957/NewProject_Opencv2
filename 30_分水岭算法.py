"""
很好的
"""
import cv2 as cv
import numpy as np


def watershed_demo(src):
    # remove noise if any
    print(src.shape)
    blurred = cv.pyrMeanShiftFiltering(src, 10, 100)      # 一般采用边缘滤波如这种滤波给要进行二值化的图像除去噪音的效果很好，不行就用高斯模糊试试
    # gray\binary image
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("binary-image", binary)

    # morphology operation
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    mb = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel, iterations=3)            # 通过形态学的操作进一步除去二值化图像中的黑点    iterations好像是表示进行几次开操作
    sure_bg = cv.dilate(mb, kernel, iterations=3)                        # 在开操作后进行一次膨胀？
    "开操作后的图像"
    cv.imshow("mor->open->dilate", sure_bg)

    # distance transform
    """
    Opencv中distanceTransform方法用于计算图像中每一个非零点距离离
    自己最近的零点的距离，distanceTransform的第二个Mat矩阵参数dst
    保存了每一个点与最近的零点的距离信息，图像上越亮的点，代表了离零点的距离越远。"""
    dist = cv.distanceTransform(mb, cv.DIST_L2, 3)                      # 距离变换，有好多种距离变换方法cv.DIST_L2
    dist_output = cv.normalize(dist, 0, 1.0, cv.NORM_MINMAX)          # 可以将距离变换的结果很好的显示出来
    cv.imshow("dist", dist)
    cv.imshow("distance-t", dist_output*50)

    "得到的surface是最亮处值得0.6倍，以此为分割点将图像分成黑白两色"
    ret, surface = cv.threshold(dist, dist.max()*0.6, 255, cv.THRESH_BINARY)         # 得到marks
    surface_fg = np.uint8(surface)                      # 得到种子
    cv.imshow("surface-bin", surface_fg)

    unknown = cv.subtract(sure_bg, surface_fg)
    ret, markers = cv.connectedComponents(surface_fg)           # connectedComponents()仅仅创建了一个标记图（图中不同连通域使用不同的标记，和原图宽高一致）

    # watershed transform
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv.watershed(src, markers=markers)
    src[markers==-1] = [0, 0, 255]
    cv.imshow("result", src)


print("--------- Python OpenCV Tutorial ---------")

src = cv.imread(r"D:\Users\acer\Desktop\phtots\111.png")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
watershed_demo(src)
cv.waitKey(0)

cv.destroyAllWindows()