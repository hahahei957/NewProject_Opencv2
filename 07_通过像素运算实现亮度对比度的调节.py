"""
所以图像混合就是将两个图像按照一定的比例转存到另一个图像中。

2、API：addWeighted（）
API参数解释
下面是对应参数的介绍：

参数1：输入图像Mat – src1

参数2：输入图像src1的alpha值（所占比重）                          # alpha是对比度的意思    但我感觉这里的alpha还是改变图片的亮度

参数3：输入图像Mat – src2

参数4：输入图像src2的beta值（所占比重）

参数5：gamma值

参数6：输出混合图像

参数7：默认参数

注意点：两张图像的大小和类型必须一致才可以。
————————————————
版权声明：本文为CSDN博主「水亦心」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/shuiyixin/article/details/89343386
"""
import cv2 as cv
import numpy as np


def contrast_brightness_color(image, contrast, brightness):
    h, w, ch = image.shape
    blank = np.zeros([h, w, ch], image.dtype)            # 我感觉image.dtype的意思是，让创建的blank的类型和image的类型一致

    dst = cv.addWeighted(image, contrast, blank, 1-contrast, brightness)
    cv.imshow("image", image)
    cv.imshow("blank", blank)
    cv.imshow("destion", dst)


image = cv.imread("beautyful_view.jpg")

contrast_brightness_color(image, 1.2, 10)

cv.waitKey(0)