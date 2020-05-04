import cv2 as cv
import numpy as np


def edge(image):
    blurred = cv.GaussianBlur(image, (3, 3), 0)
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)

    xgrad = cv.Sobel(gray, cv.CV_16SC1, 1, 0)
    ygrad = cv.Sobel(gray, cv.CV_16SC1, 0, 1)
    # edge_putput = cv.Canny(xgrad, ygrad, 50, 100)
    edge_output = cv.Canny(xgrad, ygrad, 50, 150)
    cv.imshow("edge_output", edge_output)
    return edge_output

"对得到的边缘图像(也就是一个二值图像)进一步处理"
def contours_demo(image):
    """blurred = cv.GaussianBlur(image, (3, 3), 0)
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("binary", binary)"""
    binary = edge(image)

    # contours：轮廓  heriachy：层次信息  得到的图像是由很多层次组成的
    # cv.RETR_EXTERNAL或cv.RETR_TREE都行，我认为cv.RETR_TREE包含了内部轮廓，cv.RETR_EXTERNAL质保函外部轮廓，所以cv.RETR_EXTERNAL方法挺好用的
    contours, heriachy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        cv.drawContours(image, contours, i, (0, 0, 255), 2)     # 将contours的第i层边缘填充给image上

    cv.imshow("detect contours", image)

src = cv.imread(r"coin.jfif")
cv.imshow("hello world", src)
contours_demo(src)
cv.waitKey(0)  # 显示图片时用
cv.destroyAllWindows()

