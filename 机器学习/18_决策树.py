import pandas as pd
# model_selection该类应用于各种数据分割，包括交叉验证中对数据分割成cv组，不断进行测试，来更好的评测某个模型
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier            # ensemble:全体的
# metrics是度量评估一类的意思
from sklearn.metrics import classification_report


def decision():
    # 读入数据
    # titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")    # 感觉可能是python链接网络有问题
    titan = pd.read_csv(r"D:\Users\acer\Desktop\titanic.txt")

    print(1)
    # 数据处理，处理数据内容
    # 取值是一定注意按照下面的格式，否则就是x行y列了
    x_feature = titan[['pclass', 'age', 'sex']]
    y_target = titan['survived']  # titan[['survived']]应该也可以
    # 缺失值处理
    x_feature['age'] = x_feature['age'].fillna(x_feature['age'].mean())

    x_train, x_test, y_train, y_test = train_test_split(x_feature, y_target, test_size=0.25)

    # 特征值处理，提取出特征和将特征数值化，
    # 这里我们不用提取特征值，因为特征值已经有了，我们只要将其数值化就行
    # 弄成方便机器学习的格式ont-hot编码     DictVectorizer字典特征提取器  ==》 https://www.cnblogs.com/Lin-Yi/p/8973252.html
    dic = DictVectorizer(sparse=False)    # 其中sparse=False表示不产生稀疏矩阵
    """DataFrame.to_dict(orient='dict')
    将DataFrame格式的数据转化成字典形式  ==>  https://blog.csdn.net/llx1026/article/details/77929287"""
    x_train = dic.fit_transform(x_train.to_dict(orient='records'))
    x_test = dic.transform(x_test.to_dict(orient='records'))
    print(dic.get_feature_names())

    # 使用决策树进行预测
    dec = DecisionTreeClassifier(criterion='gini')
    dec.fit(x_train, y_train)
    y_predict = dec.predict(x_test)

    # 对结果进行评估
    print(f"预测的准确率：{dec.score(x_test,y_test)}")
    print(f"进行精准率和回收率评估：{classification_report(y_test,y_predict)}")

    print("====================随机森林=============")
    # 使用随机森林 (对超参数进行调优)
    forest = RandomForestClassifier()           # 在这里就不用填参数了，直接在网格搜索交叉验证中填入随机森林模型的参数，方便进行结果验证

    param = {"n_estimators":[120, 200, 300, 500, 800, 1200], "max_depth":[5, 8, 15, 25, 30]}

    # 通过网格搜索和交叉验证,调整cv的值可以调整交叉验证分割的组数
    gc = GridSearchCV(estimator=forest, param_grid=param,cv=3)
    # 开始预测
    gc.fit(x_train,y_train)
    print(f"随机森林准确率：{gc.score(x_test,y_test)}")

decision()
