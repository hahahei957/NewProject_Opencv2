"""
对于矩阵的处理不熟悉
对于image对象的理解不够深刻
无法对image对象的局部进行处理

show_center_To_user这个函数好好看看， 气死我了

整个图像是一个三维矩阵，可以理解为三个通道，每个通道是一个二维矩阵（也可以看做一个二维矩阵中的每个成员都是一个有三个元素的数组）

"""

import cv2 as cv
import numpy as np


# 将中心范围区域中的图像填充成黑色用于标定我们获取图像的中心点给用户观测
def show_center_To_user(copy_frame):
    h, w = copy_frame.shape[:2]
    # [int(h/2-10):int(h/2+10), int(w/2-10):int(w/2+10)]
    center = np.zeros([10, 10, 3], np.uint8)
    center[:, :, 0] = 0
    center[:, :, 1] = 165
    center[:, :, 2] = 255

    copy_frame[int(h/2-5):int(h/2+5), int(w/2-5):int(w/2+5)] = center
# 用于检测show_center_To_user()函数
# src = cv.imread(r"beautyful_view.jpg")
# show_center_To_user(src)
# cv.imshow("hello world", src)
# cv.waitKey(0)                  # 显示图片时用
# cv.destroyAllWindows()

def frame_handle(frame_mask, count):
    # 获取中心区域的像素值
    # 这里获取的像素值没啥用， 我们只需要获取目标地点的位置即可， 目标位置的像素值cv.floodFill函数会自动获取
    h, w = frame_mask.shape[:2]
    value = frame_mask[int(h / 2), int(w / 2)]
    if count == 9:
        print(count, "############")
        print(value)
        value_tuple = tuple(value)
        print("_______________", value_tuple)
    # 创建掩模
    mask = np.zeros([h+2, w+2], np.uint8)
    # 通过泛红填充实现
    # 不知道为啥， 所要选区的目标像素点的高和宽的位置要取反
    frame_mask -= 100
    cv.imshow("before  floodfill", frame_mask)
    cv.floodFill(frame_mask, mask, (int(w / 2), int(h / 2)), (255, 255, 255), (50, 50, 50), (80, 80, 80), cv.FLOODFILL_FIXED_RANGE)

# src = cv.imread(r"beautyful_view.jpg")
# frame_handle(src)
# cv.imshow("hello world", src)
# cv.waitKey(0)                  # 显示图片时用
# cv.destroyAllWindows()

# def show_target(frame, frame_mask):
#     target_mask = cv.bitwise_not(frame_mask)                            # 通过像素取反函数实现
#     cv.imshow("target_1", target_mask)
#     print(frame_mask, "++++++++++++++++++++++++++++++++处理前+++++++++++")
#     target_mask =frame_mask-1000                            # 这句是不对的， 我们是要对每一个点的像素值进行处理， 而不是每一个点
#     print(target_mask, "+++++++++++++++++++++处理之后")
#     target_mask = target_mask*255
#     print(target_mask, "+++++++++++++++++++++处理之后")
#     # target = cv.bitwise_and(frame, frame, mask=target_mask)
#     cv.imshow("target_2", target_mask)
#     # cv.imshow("target______________", target)
#     # return target

def show_target(frame, frame_mask):
    dst = cv.GaussianBlur(frame_mask, (3, 3), 0)
    gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 250, 255, cv.THRESH_BINARY)  # 生成二值化图像
    target = cv.bitwise_and(frame, frame, mask=binary)
    cv.imshow("target______________", target)
    # cv.imshow("target______________", binary)
    # return binary

# src = cv.imread(r"beautyful_view.jpg")
# fra = 1
# show_target(fra, src)
# cv.imshow("hello world", src)
# cv.waitKey(0)                  # 显示图片时用
# cv.destroyAllWindows()

# 主函数
def extract_main_object():
    capture = cv.VideoCapture(0)
    count = 1
    while True:
        count += 1
        if count == 10:
            count = 0
        ret_boot, frame = capture.read()
        cv.flip(frame, 1)
        copy_frame = frame.copy()
        mask_frame = frame.copy()
        # 将中心范围区域中的图像填充成黑色用于标定我们获取图像的中心点给用户观测
        show_center_To_user(copy_frame)
        cv.imshow("showToUserToModifyFacesEdge", copy_frame)
        # 获取中心点的像素值， 并进行通过泛红填充将中心区域填充成白色
        frame_handle(mask_frame, count)
        cv.imshow("frame_handle", mask_frame)
        # 通过取遮罩层将中间的像素单独显示出来
        show_target(frame, mask_frame)
        # target = show_target(frame, mask_frame)
        # cv.imshow("target", target)

        cv.waitKey(50)
        # 处理影像的循环函数中一定不要出现cv.destroyAllWindows()这个函数，否则每个循环中都会重复打开关闭的操作
        # cv.destroyAllWindows()

extract_main_object()