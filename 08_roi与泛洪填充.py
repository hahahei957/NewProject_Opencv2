import cv2 as cv
import numpy as np


# 获取图片的一小部分进行展示
def extreat_partial(image):
    h, w = image.shape[:2]            # 取image.shape的前两位参数
    print(image.shape)
    center_face_1 = image[int(h/2)-50:int(h/2)+50, int(w/2)-50:int(w/2)+50, 0]
    center_face_2 = image[int(h/2)-50:int(h/2)+50, int(w/2)-50:int(w/2)+50, 1]

    "我觉得这样加和后，仍是一个三通道，但是三个通道的值是相同的，相当于这是一个灰度图"
    center_face = cv.add(center_face_1, center_face_2)
    cv.imshow("center", center_face)
    cv.imshow("orginal", image)


# 局部像素取灰白模式
def partial_gray(image):
    h, w = image.shape[:2]            # 取image.shape的前两位参数
    center_face = image[int(h/2)-50:int(h/2)+50, int(w/2)-50:int(w/2)+50]
    center_gray = cv.cvtColor(center_face, cv.COLOR_BGR2GRAY)
    # 我们需要将gray装换成RGB， 然后才能给image对应的区域进行赋值
    image[int(h/2)-50:int(h/2)+50, int(w/2)-50:int(w/2)+50] = cv.cvtColor(center_gray, cv.COLOR_GRAY2BGR)
    cv.imshow("gray_backface", image)


# 了OpenCV填充算法中漫水填充算法
"""
所谓漫水填充，简单来说，就是自动选中了和种子点相连的区域，接着将该区域替换成指定的颜色，
这是个非常有用的功能,经常用来标记或者分离图像的一部分进行处理或分析.漫水填充也可以用来
从输入图像获取掩码区域,掩码会加速处理过程,或者只处理掩码指定的像素点.
类似于ps中的魔棒工具
第二个参数， InputOutputArray类型的mask，这是第二个版本的floodFill独享的参数，
表示操作掩模,。它应该为单通道、8位、长和宽上都比输入图像 image 大两个像素点的图像。
第二个版本的floodFill需要使用以及更新掩膜，所以这个mask参数我们一定要将其准备好并
填在此处。需要注意的是，漫水填充不会填充掩膜mask的非零像素区域。例如，一个边缘检测算
子的输出可以用来作为掩膜，以防止填充到边缘。同样的，也可以在多次的函数调用中使用同一个
掩膜，以保证填充的区域不会重叠。另外需要注意的是，掩膜mask会比需填充的图像大，所以 ma
sk 中与输入图像(x,y)像素点相对应的点的坐标为(x+1,y+1)
———————————————— 
版权声明：本文为CSDN博主「浅墨_毛星云」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。             -->
原文链接：https://blog.csdn.net/poem_qianmo/article/details/28261997
版权声明：本文为CSDN博主「浅墨_毛星云」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/poem_qianmo/article/details/28261997

看一看上面链接的文章
FLOODFILL_FIXED_RANGE - 如果设置为这个标识符的话，就会考虑当前像素与种子像素之间的差，否则就考虑当前像素与其相邻像素的差。也就是说，这个范围是浮动的。
FLOODFILL_MASK_ONLY - 如果设置为这个标识符的话，函数不会去填充改变原始图像 (也就是忽略第三个参数newVal), 而是去填充掩模图像（mask）。这个标识符只对第二个版本的floodFill有用，因第一个版本里面压根就没有mask参数。
"""
def fill_color_demo(image):
    copyIMG = image.copy()
    h, w = image.shape[:2]
    # mask在这里作为遮罩层使用
    mask = np.zeros([h+2, w+2, 1], np.uint8)             # h+2, w+2是硬性规定， 1表示这是一层的二维矩阵。 也就是说这个图像是单通道的
    copyIMG[int(h / 2) + 100:int(h / 2) + 105, int(w / 2) + 50:int(w / 2) + 55, :] = 255
    # 取(int(h/2)+100, int(w/2)+150)点为起始点， 用(0,0,0)黑色填充， 选择像素范围最小是当前像素值-100到+50的范围
    cv.floodFill(copyIMG, mask, (int(h/2)+100, int(w/2)+50), (0, 0, 0), (50, 50, 50), (100, 100, 100), cv.FLOODFILL_FIXED_RANGE)
    cv.imshow("target", copyIMG)
    cv.imshow("orignal", image)


src = cv.imread(r"beautyful_view.jpg")

cv.imshow("hello world", src)
extreat_partial(src)
partial_gray(src)
fill_color_demo(src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()
