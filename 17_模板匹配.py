"""https://blog.csdn.net/liyuanbhu/article/details/49837661"""

import cv2 as cv
import numpy as np


def template_demo():
    tpl = cv.imread("soccer_local.png")
    target = cv.imread("soccer_target.png")
    cv.imshow("template image", tpl)
    cv.imshow("target image", target)
    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = tpl.shape[:2]
    for md in methods:
        print(md)
        # result获得的是一个矩阵。通过后面选择的md比较方式的不同， 图像分别在最值处取得最佳匹配结果
        result = cv.matchTemplate(target, tpl, md)
        print(f"result:{result}")
        # cv.minMaxLoc的min_val和max_val是获取图像中的最值用的，min_loc和max_loc是获取某一最值点的位置用的
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        """因为cv.TM_SQDIFF_NORMED该匹配方式获得的值越小越好，另外两个方式匹配的值越大越好,所以当用的是cv.TM_SQDIFF_NORMED方法时，取最小值"""
        if md == cv.TM_SQDIFF_NORMED:
            tl = min_loc               # 矩阵中最小值的位置
        else:
            tl = max_loc                # 矩阵中最大值的位置
        # 矩形框的最大边界点的坐标
        br = (tl[0]+tw, tl[1]+th)
        print(f"t1:==========={max_loc}")
        """cv.rectangle:画矩形的工具  -->  https://blog.csdn.net/chentravelling/article/details/44945303"""
        cv.rectangle(target, tl, br, (0, 0, 255), 2)        #
        cv.imshow("match-"+np.str(md), target)
        cv.imshow("match-ha" + np.str(md), result)


print("--------- Python OpenCV Tutorial ---------")

template_demo()
cv.waitKey(0)

cv.destroyAllWindows()