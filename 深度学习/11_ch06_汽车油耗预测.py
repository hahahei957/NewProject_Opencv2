
import os


import pandas as pd
import tensorflow as tf
from tensorflow import keras

"""
这个问题不同于前面的分类问题，而是一个目标值连续的问题
"""
# 得到数据集
def load_data():
    # 在线下载汽车效能数据集到C:\Users\acer\.keras\datasets\auto-mpg.data中
    dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")

    # 效能（公里数每加仑），气缸数，排量，马力，重量 加速度，型号年份，产地
    # column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight','Acceleration', 'Model Year', 'Origin']
    column_names = ['效能(多少公里一加仑)', '气缸数', '排量', '马力', '重量', '加速度', '型号年份', '产地']

    # names指定每一列对应的名字，na_values指定空值、comment貌似是以\t开头的行会被剔除、sep指定分隔符, skipinitialspace忽略分隔符后的空白（默认为False，即不忽略）
    raw_dataset = pd.read_csv(dataset_path, names=column_names, na_values='?', comment='\t', sep=' ', skipinitialspace=True)

    dataset = raw_dataset.copy()
    return dataset

def preprocess_dataset(dataset):
    dataset = dataset.copy()
    # 统计空白数据,并清除
    dataset = dataset.dropna()

    # 处理类别性数据，其中origin列代表了类别1,2,3,分布代表产地：美国、欧洲、日本
    # 其弹出这一列
    origin = dataset.pop('产地')
    # 根据origin列写入新列
    dataset['USA'] = (origin == 1) * 1.0
    dataset['Europe'] = (origin == 2) * 1.0
    dataset['Japan'] = (origin == 3) * 1.0

    # 通过pandas自带的随机抽样方法进行抽样
    train_dataset = dataset.sample(frac=0.8, random_state=0)     # 随机选取若干行，frac是抽取的比例
    test_dataset = dataset.drop(train_dataset.index)               # 这个就是根据索引删除目标行，剩下的20%就是测试数据

    # 获取数据集的统计信息  通过describ方法可以的到每个标签的方差、均值等
    train_stats = train_dataset.describe()
    # 效能MPG是我们训练模型要去拟合的目标值，所以在这里没有啥意义，所以从统计中除去,剩下的就是我们需要的特征值了
    train_stats.pop("效能(多少公里一加仑)")
    print("============train_stats:(通过describ方法可以的到每个标签的方差、均值等如下)\n",train_stats) # 通过describ方法可以的到每个标签的方差、均值等
    # 训练集和测试集的数据集都去掉MPG列，单独取出作为标注
    train_y = train_dataset.pop('效能(多少公里一加仑)')
    test_y = test_dataset.pop('效能(多少公里一加仑)')
    # print("===============train_y===\n", train_y[:10])
    # print("===============test_y===\n", test_y[:10])
    # 通过pop去除目标预测值(效能MPG)的train_dataset就只剩下特征值了
    train_x = train_dataset
    test_x = test_dataset

    # 对统计结果做行列转置，方便将统计结果作为下面做数据规范化的参数
    train_stats = train_stats.transpose()  # 这里进行的转置，一定要注意
    print("============train_stats[mean]:", train_stats['mean'], "train_stats", train_stats)
    # 正则化   就是将数据减去均值再除以方差，也就是类似于正态分布的标准化，我感觉这样就是类似于特征处理中的标准化
    train_x = (train_x-train_stats['mean'])/train_stats['std']
    test_x = (test_x-train_stats['mean'])/train_stats['std'] # 在这里进行正则化后，使他们初始自身所带有的权重变为0，后面再在网络中给他们赋予权重

    return train_x, test_x, train_y, test_y

# 构件网络层
def build_model(train_x):
    print(len(train_x.keys()), "=======len(train_x.keys())")
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=[len(train_x.keys())]),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)                # 全输出层，由于这里不是分类算法，所以输出结果是一个预测的连续值
    ])

    # 优化器（梯度下降算法的优化器
    optimizer = keras.optimizers.RMSprop(0.01)

    model.compile(
        loss='mse',    # mse-均方误差、mae-平均绝对误差(平均绝对误差是所有单个观测值与算术平均值的偏差的绝对值的平均)、、、
        optimizer=optimizer,
        metrics=['acc']
    )
    return model

def main():
    dataset = load_data()
    train_x, test_x, train_y, test_y = preprocess_dataset(dataset)
    model = build_model(train_x)
    # 显示构造的模型
    model.summary()

    EPOCHS=1000
    # fit中的参数：
    #       validation_split用于在没有提供验证集的时候，按一定比例从训练集中取出一部分作为验证集      https://blog.csdn.net/Mr_Brooks/article/details/80277114
    #       verbose：日志显示    https://blog.csdn.net/my_kingdom/article/details/84313683
    history = model.fit(
        train_x, train_y, epochs=EPOCHS, validation_split=0.2, verbose=1
    )

    # 使用测试集预测数据
    predict = model.predict(test_x)
    # 显示预测结果
    print("==============test:\n", test_y, '===================\npredict:', predict)


if __name__ == '__main__':
    main()



