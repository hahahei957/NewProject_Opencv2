
# 前向传播实战的示例代码

import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt

# 加载数据
def load_data():
    # 加载数据集
    (x_train, y_train),(x_test,y_test) = keras.datasets.mnist.load_data()
    # 将数据转换成浮点张量, 并缩放到-1~1
    x_train = tf.convert_to_tensor(x_train, dtype=tf.float32)/255
    # 将y转为整形张量
    y_train = tf.convert_to_tensor(y_train, dtype=tf.int32)

    # 将分类结果y改成one-hot编码
    y_train = tf.one_hot(y_train, depth=10)

    # 改变视图， [b, 28, 28] => [b, 28*28]
    x_train = tf.reshape(x_train, (-1, 28*28))

    # 加载数据   使用 tf.data.Dataset.from_tensor_slices 进行加载数据集.
    train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    # 批量训练
    train_dataset = train_dataset.batch(200)        # 将train_dataset中的60000个数据分成300份，每份200个样本
    return train_dataset

# 初始化网络层
# 每个样本都乘以相同的权重值，在加上一个bias
def init_paramaters():
    # 每层的张量都需要被优化，故使用 Variable 类型，并使用随机正太分布初始化权值张量
    # 偏置向量初始化为 0 即可
    # 第一层： [b, 28*28]@[28*28, 256] ==> [b, 256]
    w1 = tf.Variable(tf.random.truncated_normal([28*28, 256], stddev=0.1))
    b1 = tf.Variable(tf.zeros([256]))
    # 第二层： [b, 256]@[256*128] ==>  [b, 128]
    w2 = tf.Variable(tf.random.truncated_normal([256, 128], stddev=0.1))
    b2 = tf.Variable(tf.zeros([128]))
    # 第三层： [b, 128]@[128, 10] ==>  [b, 10]
    w3 = tf.Variable(tf.random.truncated_normal([128, 10], stddev=0.1))
    b3 = tf.Variable(tf.zeros([10]))
    return w1, b1, w2, b2, w3, b3


# 进行训练优化权重的函数
def train_epoch(epoch, train_dataset, w1, b1, w2, b2, w3, b3, lr=0.001):
    for step, (x_train, y_train) in enumerate(train_dataset):    # train_dataset共有60000个样本，通过batch按照200份一组分成了300组，所以这里循环300次
        with tf.GradientTape() as tape:
            # 第一层的计算   [b, 784]@[784, 256] + [256] => [b, 256] + [256] => [b,256] + [b, 256]
            h1 = x_train@w1 + tf.broadcast_to(b1, [x_train.shape[0], 256])     # 将偏距b1映射到b行256列的数据中,即[256] ==>  [b, 256], 这个银蛇好像可有可无
            h1 = tf.nn.relu(h1)  # 通过激活函数，增加网络的非线性
            # 第二层计算     [b, 256] => [b, 128]
            h2 = h1@w2 + b2   # 上面对于b1的映射好像可有可无
            h2 = tf.nn.relu(h2)  # 增加网络的非线性
            # 第三层，也就是输出层的计算   [b, 128] => [b, 10]
            out = h2@w3 + b3

            # 计算网络输出与标签之间的均方差， mse = mean(sum(y-out)^2)
            loss = tf.reduce_mean(tf.square(y_train - out))         # 注意：这里没用求和除以样本数量，直接求得均值
            # 自动梯度，需要求梯度的张量有[w1, b1, w2, b2, w3, b3]
            grads = tape.gradient(loss, [w1, b1, w2, b2, w3, b3])

        # 梯度更新， assign_sub函数是将当前值减去参数值，原地更新
        w1.assign_sub(lr*grads[0])
        b1.assign_sub(lr * grads[1])
        w2.assign_sub(lr * grads[2])
        b2.assign_sub(lr * grads[3])
        w3.assign_sub(lr * grads[4])
        b3.assign_sub(lr * grads[5])

    return loss.numpy()            # 将数据转换为numpy类型的数据

# 主程序
def train():
    loss_list = list()
    train_dataset = load_data()                             # 载入数据，创建张量(变量)
    w1, b1, w2, b2, w3, b3 = init_paramaters()              # 初始化网络层
    for epoch in range(10):
        loss = train_epoch(epoch, train_dataset, w1, b1, w2, b2, w3, b3)   # 用同一组数据重复训练模型
        loss_list.append(loss)
        print(loss)

    x = [i for i in range(len(loss_list))]
    plt.plot(x, loss_list)
    plt.xlabel("Epoch")
    plt.ylabel("MSE")
    plt.savefig("09_MNIST数据集的前向传播训练误差曲线.png")
    plt.show()


if __name__=="__main__":
    train()




