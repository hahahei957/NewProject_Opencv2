# 导入库
import tensorflow as tf
import numpy as np
from tensorflow import keras

"""
整个过程可分为五步：
1创建Sequential模型，2添加所需要的神经层，3使用.compile方法确定模型训练结构，4使用.fit方法使模型与训练数据“拟合”，5.predict方法进行预测。
"""

# 定义和编译一个神经网络
# tf.keras.Sequential 创建模型
# keras.layers.Dense定义每一层的配置，具体看后面的链接，讲的非常好 ==》https://blog.csdn.net/weixin_42499236/article/details/84624195
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])    # input_shape是输入数据的形状
# 编译 并指定 loss optimizer
# optimizer:优化器，应该就是梯度下降一类的 ==》 https://blog.csdn.net/weixin_41417982/article/details/81561210
# lose指定损失函数(或者说是被优化函数)，这里用的是均方误差（预测值与真实值之差的平方和的平均值,不同于方差）
model.compile(optimizer='sgd', loss='mean_squared_error')
# 提供数据
xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)
# 迭代训练次数
model.fit(xs, ys, epochs=500)    # fit的数据可能只要float类型
# 预测
print(model.predict([10.0]))