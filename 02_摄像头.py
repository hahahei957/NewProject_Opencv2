import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0)    # 0.1.2.3...表示我们配置的摄像头， VideoCapture（）的括号中也可以添加路径获取电脑中的一些影像
cv.namedWindow("摄像头", cv.WINDOW_AUTOSIZE)

while True:
    ret, frame = capture.read()  # 这句话一定要在循环里面，循环一次， 从摄像头中读一次值

    # frame代表第几帧(学习视频中是这样说的)，但是frame的类型和01_HelloWorld中的图片的类型都一样，都是<class 'numpy.ndarray'>
    # 而ret的类型则是布尔型，即<class 'bool'>

    cv.flip(frame, 1)
    # 将获得的图像镜像一下

    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # COLOR_BGR2GRAY中的BGR2GRAY表示将RGB3通道转换为GRAY灰白模式单通道的

    src = frame.copy()
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)          # 通过使用特殊的矩阵可以实现图像通过自定义的模糊使得图像变得锐化清晰
    dst = cv.filter2D(src, ddepth=-1, kernel=kernel)
    # dst = cv.bilateralFilter(src, 0, 100, 15)
    cv.imshow("rui hua hou de tu xiang", dst)

    cv.imshow("摄像头", frame)
    c = cv.waitKey(50)
    # 貌似延迟5ms，是要控制while循环的单次循环为50ms， 也就可以理解为50ms刷新一次， 即50ms刷新一帧
    print("____________________1_____________")

    # 我感觉下面这两行代码没啥用处
    if c==27:
        print("___________________________2")
        break

    print(type(frame))                       # frame的类型和01_HelloWorld中的图片的类型都一样，都是<class 'numpy.ndarray'>
    print("_______________________________")
    print(type(ret))                         # ret
