# 训练集
from sklearn.datasets import fetch_20newsgroups
# 分割数据用
from sklearn.model_selection import train_test_split
# 特征提取
from sklearn.feature_extraction.text import TfidfVectorizer
# 朴素贝叶斯
from sklearn.naive_bayes import  MultinomialNB
# 得出精确率和召回率
from sklearn.metrics import classification_report
"""朴素贝叶斯善于进行文本分类
该程序通过众多文章中的词出现的频率进行统计
，从而去预测其他文章是某类文章的概率

缺点：
    无法通过超参数提升精确度、没有考虑特征之间的关联性
"""
def naviebayes():
    # 获取数据集
    news = fetch_20newsgroups(subset='all')

    # 数据分割
    x_train,x_test,y_train,y_test = train_test_split(news.data, news.target, test_size=0.25)

    # 特征处理之前x_test的样式
    print(f"x_test:{type(x_test)}")
    print(f"x_test:{x_test}")
    print("=============")

    # 文本特征抽取
    # TF表示词频，与词在文章中出现的频率成正比
    # IDF逆向文件频率，一个词在总文档中出现频率越多，其的IDF值就越小
    # 最后得到这个词出现在某类文章中的概率是两者的乘积TF*IDF
    # 具体看该文章：https://www.cnblogs.com/mengnan/p/9307648.html
    tf = TfidfVectorizer()                    # 注意这里提取特征的函数别用错了
    # 转换器
    x_train = tf.fit_transform(x_train)
    print(tf.get_feature_names())
    x_test = tf.transform(x_test)

    # 特征处理之后x_test的样式
    print(f"x_test:{type(x_test)}")
    print(f"x_test:{x_test}")
    print("=============")

    # 训练数据(即通过朴素贝叶斯计算出一个词出现在某类文章中的概率，从而得出来某个文章大概属于哪个类别)
    mlt = MultinomialNB(alpha=1.0)     # alpha这个值是防止出现概率为零的情况，让出现概率为零的情况改成近似为零，减少误判
    mlt.fit(x_train, y_train)
    y_predict = mlt.predict(x_test)
    # 得出结果

    # 混淆矩阵
    print(f"准确率率为{mlt.score(x_test,y_test)}")         # 准确率不同于精确率
    print("每个类别的精确率和召回率",classification_report(y_test,y_predict))

naviebayes()
