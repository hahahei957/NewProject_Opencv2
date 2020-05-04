import cv2 as cv
import numpy as np


def big_binary(image):
    print(image.shape)
    h, w = image.shape[:2]

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    "将整个大图切片成多个256*256大小的区域"
    for row in range(0, h, 256):  # 从0到h-1， 步长为256
        for line in range(0, w, 256):
            "得到待处理的区域"
            roi = gray[row:row+256, line:line+256]
            print(np.std(roi), np.mean(roi))

            "去噪点, 将标准差小于15的部分设置为白色， 因为标准差小于15说明该区域像素内容几乎没有对比度"
            dev = np.std(roi)
            if dev < 15:
                gray[row:row+256, line:line+256] = 255
            else:
                ret, dst = cv.threshold(roi, 0, 255, cv.THRESH_BINARY|cv.THRESH_OTSU)
                gray[row:row+256, line:line+256] = dst
    cv.imwrite(r"haha.png", gray)


src = cv.imread(r"Aeolian.jpg")
big_binary(src)
cv.imshow("hello world", src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()
