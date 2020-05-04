"""
图像每个像素点的加减运算
"""

import cv2 as cv
import numpy as np

source = cv.imread("beautyful_view.jpg")

"""为什么得到的是三张不同d灰度图呢？不是已经分离出R，G，B通道了吗？应该是分别是红色图，绿色图，蓝色图才对阿。
原因是：当调用 imshow（R）时，是把图像的R，G，B三个通道的值都变为R的值，所以图像的颜色三通道值为（R，R，R）
同理 imshow（G）和imshow（B）所显示d图像的颜色通道也依次为（G，G，G）和（B，B，B）。
而 当三个通道d值相同时，则为灰度图。

文章不错  -->  https://blog.csdn.net/u014453898/article/details/80715121"""
b, g, r = cv.split(source)

cv.imshow("blue", b)
zeros = np.zeros(source.shape[:2], dtype="uint8");#创建与image相同大小的零矩阵
cv.imshow("real blue", cv.merge([b, zeros, zeros]))
# 通过切片也可以实现使图像另外两个通道为0      关于切片的文章  ==>  https://www.jianshu.com/p/15715d6f4dad
# 此程序第37行有关于切片的深刻利用，援引自上文
source_copy = source.copy()
source_copy[: ,: , -2:] = 0
cv.imshow("try blue", source_copy)

cv.imshow("red", r)
source[:, :, 1] = 0
cv.imshow("delt_page", source)

aim = cv.add(b, r)        # aim只有一个通道，是吗？
print(b)
cv.imshow("target_2", aim)
cv.waitKey(0)

"""
4.修改单个元素
>>>a[3] = ['A','B']
[0, 1, 2, ['A', 'B'], 4, 5, 6, 7, 8, 9]
5.在某个位置插入元素

>>>a[3:3] = ['A','B','C']
[0, 1, 2, 'A', 'B', 'C', 3, 4, 5, 6, 7, 8, 9]
>>>a[0:0] = ['A','B']
['A', 'B', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
6.替换一部分元素
>>>a[3:6] = ['A','B']
[0, 1, 2, 'A', 'B', 6, 7, 8, 9]

作者：马尔代夫Maldives
链接：https://www.jianshu.com/p/15715d6f4dad
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

"                      看到这了                          "





