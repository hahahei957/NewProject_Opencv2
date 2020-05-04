"""
形态学操作
"""

import cv2 as cv
import numpy as np

def measure(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    ret, binary = cv.threshold(gray, 250, 255, cv.THRESH_BINARY)
    print("threshold value is", ret)
    cv.imshow("binary", binary)

    dst = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
    cv.imshow("dst", dst)

    # 发现轮廓
    """  一定注意！！！cv.findContours函数处理的是二值图像， 虽然gray图像也可以处理，但优先用二值图，效果不好再用灰度图 """
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        "这个得到的是面积"
        area = cv.contourArea(contour)

        "得到轮廓的外接矩形"
        x, y, w, h = cv.boundingRect(contour)

        "画外接矩形"
        "矩形边框（Bounding Rectangle）是说，用一个最小的矩形，把找到的形状包起来。还有一个带旋转的矩形，面积会更小"
        "https://blog.csdn.net/hjxu2016/article/details/77833984"
        cv.rectangle(dst, (x, y), (x+w, y+h), (255, 255, 255), 2)
        print("x:%s    y:%s  w:%s  h:%s" % (x, y, w, h))
        cv.imshow("wai bu lun kuo", dst)

        "求出宽高比?"
        rate = min(w, h)/max(w, h)
        print("retangle rate is %s"%rate)

        # 关于原点矩和中心距的含义解释：
        "原点矩就是几何图形的重心；"
        "中心矩反映几何图形上点的分布规律，相当于将坐标原点移到重心上，此时的原点矩。"

        """统计中矩 E[(X-A)^k]的定义是各点对某一固定点A离差幂的平均值。
        如果A=0，则是原点矩，A=均值，则是中心距，K是阶数。 统计中引入矩
        是为了描述随机变量的分布的形态。 数学期望是一阶原点矩（表示分布
        重心）、方差是二阶中心距（表示离散程度）、偏态是三阶中心矩（表示
        分布偏离对称的程度）、峰态是四阶中心距（描述分布的尖峰程度，例如
        正态分布峰态系数=0）"""

        # 得到几何矩（百度说这是中心距）
        mm = cv.moments(contour)
        # 套入视频中给的公式， 得到集合图形的中心点位置
        center_x = mm["m10"]/mm["m00"]
        center_y = mm["m01"]/mm["m00"]


        "画一个实心的半径为3的圆来标记矩形中心"
        cv.circle(dst, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)


        "double epsilon：指定的精度，也即是原始曲线与近似曲线之间的最大距离。   bool closed：若为true,则说明近似曲线是闭合的，反之，若为false，则断开。"
        "https://blog.csdn.net/wangmengmeng99/article/details/72500712"
        "多边形逼近 ： 输出的点集，当前点集是能最小包容指定点集的。画出来即是一个多边形"
        approxCurve = cv.approxPolyDP(contour, 4, True)

        if approxCurve.shape[0]==4:      # 判断这个逼近出来的多边形是几边的，大于6边形则可以大概猜测为圆形
            cv.drawContours(dst, contours, i, (0, 255, 0), 2)    # 用蓝色标出
        if approxCurve.shape[0] == 4:
            cv.drawContours(dst, contours, i, (0, 0, 255), 2)    # 如果边为4个， 则用红色标出
        if approxCurve.shape[0] == 3:
            cv.drawContours(dst, contours, i, (255, 0, 0), 2)    # 如果边为3个， 则用绿色标出
        cv.imshow("measure-contours", dst)


src = cv.imread(r"D:\Users\acer\Desktop\phtots\open_06.jfif")
cv.imshow("hello world", src)
measure(src)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()





