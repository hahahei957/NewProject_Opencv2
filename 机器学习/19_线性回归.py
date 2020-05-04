from sklearn.datasets import load_boston

from  sklearn.model_selection import train_test_split           # model_selection模型选择过程中各种数据分割的类与函数

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression, SGDRegressor, LogisticRegression           # 线性回归
# externals是外部的、外部扩展的意思
from sklearn.externals import joblib             # 模型的保存和提取  ==》  https://blog.csdn.net/YZXnuaa/article/details/80694372

from sklearn.metrics import mean_squared_error, classification_report    # 均方误差的评估
import pandas as pd
import numpy as np

# 通过线性回归预测房价
# （数据量小的时候，可以用linearRegression，也就是最小二乘法之正规方程，可以直接求得误差最小点，但是计算量特别大，数据多时不推荐使用）
# 这个也就是高中学的线性方程的求解k和b的值类似的方法
def mylinear():
    # 获取数据
    lb = load_boston()
    # 特征数值化

    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)

    # 归一化处理
    """因为特征值和目标值对应的数组维度不一样， 所以无法用同一个转换器进行归一化，而是分别创造一个转换器"""
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    # 对于目标的
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))

    # 建立模型
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    print(lr.coef_)

    # 模型保存，可以在别的地方直接加载出来这次保存好的模型用来继续学习或者预测使用
    joblib.dump(lr, './通过joblib保存线性回归模型.pkl')

    # 预测结果评估
    y_predict = lr.predict(x_test)
    # 线性回归模型的好坏通过均方误差来评测
    print("产生的均方误差为：", mean_squared_error(y_test, y_predict))
    # 将数据变回归一化之前的大小
    y_predict_orign = std_y.inverse_transform(y_predict)
    print(y_predict, "==================", y_predict_orign)    # ==》产生的均方误差为： 0.42782165417388635

# 用梯度下降来预测房价,在数据量大的时候推荐使用这个
def sgd_regression():
    # 下面这些是直接从上面的函数中copy下来的
    # 获取数据
    lb = load_boston()
    # 特征数值化
    # 分割数据集
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
    # 归一化处理
    """因为特征值和目标值对应的数组维度不一样， 所以无法用同一个转换器进行归一化，而是分别创造一个转换器"""
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    # 对于目标的
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))

    # 建立模型(基于随机梯度下降法估计参数的SGDRegressor)
    sgd = SGDRegressor()

    # 预测并评估
    sgd.fit(x_train, y_train)
    y_predict = sgd.predict(x_test)
    print(mean_squared_error(y_test, y_predict))  # ==》产生的均方误差为： 0.21901470588593194


# 岭回归：也就是逻辑回归
# 只能用于解决二分类问题，属于判别模型（与前面所学的生成模型相区别，生成模型是需要从历史中总结出某些概率）
# 但我感觉对于判别模型和生成模型还是不太对

# 岭回归解觉二分类问题的思路 ==》 https://blog.csdn.net/weixin_39445556/article/details/83930186
# 先生成回归曲线，再从y轴找一个合理的值设置为阈值（临界值），求解的y值大于这个阈值的为一个结果，y小于这个阈值是另一个结果
# 阈值的选择可以根据二分类中的一类占总数量的比例
def LingHuiGui():
    # 对于癌症的预测
    # 读取数据
    column = ['Sample code number','Clump Thickness', 'Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion', 'Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class']
    data = pd.read_csv(r"E:\chrome下载的东西\breast-cancer-wisconsin.data", names=column)   # 这个指定标签名的方式一定要学一学
    print(data)

    # 缺失值处理
    data = data.replace("?", np.nan)
    data = data.dropna()

    # 数据分离                                            # data中的column是前面第89行的那个标签名列表
    x_train, x_test, y_train, y_test = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)

    # 数据标准化（归一化）
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)

    # 这里用的逻辑回归是个二分类方法，是解决二分类问题的
    # std_y = StandardScaler()
    # y_train = std_y.fit_transform(y_train)
    # y_test = std_y.transform(y_test)

    # 建立模型
    lg = LogisticRegression(C=1.0)  # c为正则化参数（正则化用于解决过拟合问题，可以减少模型的复杂度）
    lg.fit(x_train, y_train)
    y_predict = lg.predict(x_test)

    # 误差评估
    print("精确率：", lg.score(x_test, y_test))
    # 将结果为2、4两个数值换为名字良性和恶性
    print("召回率", classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"]))

print("加油！")
# mylinear()
# sgd_regression()
LingHuiGui()




