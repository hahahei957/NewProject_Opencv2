import itchat
import os
import math
from PIL import Image


# # 获取数据
# def download_image():
#     # 扫描二维码登陆微信，即通过网页版登陆微信
#
#     #
"""我的账号登不上，就先不写了"""

# 获取数据
def download_image():
    # 扫描二维码登陆微信，即通过网页版微信登陆
    itchat.auto_login()
    # 返回一个包含用户信息字典的列表
    friends = itchat.get_friends(update=True)
    #  在当前位置创建一个用于存储头像的目录wechatImages
    base_path = './wechatImages'
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    # 获取所有好友头像
    for friend in friends:
        # 获取头像数据
        img_data = itchat.get_head_img(userName = friend['UserName'])
        #判断备注名是否为空
        if friend['RemarkName'] != '':
            img_name = friend['RemarkName']
        else :
            img_name = friend['NickName']
         #   在实际操作中如果文件名中含有*标志，会报错。则直接可以将其替换掉
        if img_name is "*":
            img_name = ""
        #通过os.path.join()函数来拼接文件名
        img_file = os.path.join(base_path, img_name + '.jpg')
        print(img_file)
        with open(img_file, 'wb') as file:
            file.write(img_data)


# 拼接头像
def join_image():
    base_path = './headImages'
    files = os.listdir(base_path) #返回指定的文件或文件夹的名字列表
    print(len(files))
    each_size = int(math.sqrt(float(6400 * 6400) / len(files)))#计算每个粘贴图片的边长
    lines = int(6400 / each_size)#计算总共有多少行
    print(lines)
    image = Image.new('RGB', (6400, 6400))# new(mode, size, color=0) 定义一张大小为640*640大小的图片，不给出第三个参数默认为黑色
    x = 0 #定义横坐标
    y = 0 #定义纵坐标
    for file_name in files:
        img = Image.open(os.path.join(base_path, file_name)) #找到/打开图片
        img = img.resize((each_size, each_size), Image.ANTIALIAS)#实现图片同比例缩放，Image.ANTIALIAS添加滤镜效果
        image.paste(img, (x * each_size, y * each_size))#将缩放后的照片放到对应的坐标下
        x += 1
        if x == lines:#如果每行的粘贴内容够了，则换行
            x = 0
            y += 1
    image.save('jointPic.jpg')#最后将全部的照片保存下来

if __name__ == '__main__':
    download_image()
    join_image()
