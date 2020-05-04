import jieba
import wordcloud
import matplotlib.image as mping  # mping用于读取数据
import os

f = open(r"E:\pycharm\NewProject_Opencv\aiqiyi\歌手·当打之年之华晨宇一生只唱一次的歌 周深狂野《Monsters》-综艺-高清正版视频在线观看–爱奇艺.txt",
         "r", encoding='utf-8')
content = f.read()
f.close()
ls = jieba.lcut(content)                            # 将文本中的关键字根据出现频率提取出来
# 将单词拼接成字符串
text = '  '.join(ls)                                # 用中文生成词云图时，需要先分词并组成空格分隔字符串

def transimg(img_path):                             # 这样转换出来的照片不能用来imread处理了，所以建议不用
    if img_path.endswith('jpg'):
        new_img_path = img_path.split(".")[0] + ".png"
        os.rename(img_path, new_img_path)           # 改文件的名字
        return new_img_path
    return img_path


# 通过matplotlib弄出来遮罩层(貌似准确说应该是显示区域)
# file = "D:/Users/acer/Desktop/所有的文件/大数据课件/大数据第4章/ch4案例资料/heart.png"
# file = transimg(file)
# mask = mping.imread(file)
mask = mping.imread("D:/Users/acer/Desktop/所有的文件/大数据课件/大数据第4章/ch4案例资料/heart.jpg")

"""
# 输出的图片必须是png，而jpg图片无法直接转换为jpg，所以输入必须是输入的图片必须是png
w = wordcloud.WordCloud(width=800, height=600,
                        # 因为api中显示mode缺省为RGB，所以看了一下他的api，发现他可以设置背景透明
                        # mode : string (default="RGB")
                        #         Transparent background will be generated when mode is "RGBA" and
                        #         background_color is None.
                        mode="RGBA", background_color=None,
                        font_path='C:/Users/acer/AppData/Local/Microsoft/Windows/Fonts/锐字锐线怒放黑简1.0.TTF',
                        scale=32,                  # 调整图片清晰度：scale属性，该值越大越清楚，我设置的是scale=32。
                        mask=mask)
"""

w = wordcloud.WordCloud(width=800, height=600,
                        background_color="white", font_path='C:/Users/acer/AppData/Local/Microsoft/Windows/Fonts/锐字锐线怒放黑简1.0.TTF',
                        # 增大scale的值之后，生成图片的时间变长了
                        scale=32,                  # 调整图片清晰度：scale属性，该值越大越清楚，我设置的是scale=32。
                        mask=mask)

w.generate(text)
w.to_file("./弹幕4.jpg")