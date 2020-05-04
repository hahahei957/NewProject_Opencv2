"""
cvWaitKey(int delay) 指延时delay ms的时间

delay<=0时，函数cvWaitKey无限制的等待按键事件，所以显示图像时，需要在cvShowImage("**.bmp",image)后加上cvWaitKey(n)——n为小于等于0的数即可，程序停在显示函数处，不运行其他代码;否则，图像无法正常显示。

delay>0时，延迟"delay"ms，在显示视频时这个函数是有用的，用于设置在显示完一帧图像后程序等待"delay"ms再显示下一帧视频；如果使用cvWaitKey(0)则只会显示第一帧视频。



返回值：被按键的值，如果超过指定时间则返回-1。
        如果程序想响应某个按键，可利用if(cvWaitKey(1)==Keyvalue)；

经常程序里面出现if( cvWaitKey(10) >= 0 ) 是说10ms中按任意键退出
"""

import cv2 as cv

src = cv.imread(r"Aeolian.jpg")                                # 不知为啥，这里的路径存在问题，一直采用绝对路径，一直报错，说路径不对
# 如果不建立窗口的话，后面的imshow无法指定要显示的窗口，导致图片无法显示
# 不仅如此，我们再建立窗口时，还要指定窗口的大小
# 更正：貌似不建立窗口也可以将照片显示出来
cv.namedWindow("hello world", cv.WINDOW_AUTOSIZE)
# 用我们新创建的窗口展示我们想要展示的照片
cv.imshow("hello world", src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()

print("________________")
print(type(src))                          # <class 'numpy.ndarray'>
print("________________")







import cv2 as cv
import numpy as np

"""
读取的路径名字一定不能含有中文
"""
src = cv.imread(r"beautyful_view.jpg")

cv.imshow("hello world", src)
cv.waitKey(0)                  # 显示图片时用
cv.destroyAllWindows()



import cv2
import numpy as np
img_path = r"G:\Python_work\图片\vikings.jpg"
#img = cv2.imread(r"G:\Python_work\图片\vikings.jpg")
img = cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
#也可以写成cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),-1)；
# cv2.IMREAD_UNCHANGED参数可以用-1代替
#cv2.IMREAD_GRAYSCALE:以灰度模式读入图像：其值为0
#cv2.IMREAD_COLOR:读入彩色图像：其值为1；
#np.fromfile()函数相对应的函数为np.tofile()
img_write = cv2.imencode(".jpg",img)[1].tofile(img_path)
#cv2.imencode()函数返回两个值;写入成功返回Ture，另一个值为数组.
#_,im_encode = cv2.imencode(".jpg",img)
cv2.imshow("img",img)
cv2.waitKey()


