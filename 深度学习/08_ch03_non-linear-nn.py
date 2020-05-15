import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt

"""数据集的路径       C:/Users/acer/.keras/datasets        """
# 加载 mnist数据集
# 我感觉x,y是训练集、x_val\y_val是预测集
# (x, y), (x_val, y_val) = keras.datasets.mnist.load_data()
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
# 转换为浮点张量， 并缩放到-1~1
x_train = tf.convert_to_tensor(x_train, dtype=tf.float32) / 255
# 转换为整形张量
y_train = tf.convert_to_tensor(y_train, tf.int32)

# print(x[:100])
print(y_train)
print("================="*2)
print(y_train.shape)
print("================="*2)
# print(x_val[:100])
print("================="*2)
print(y_test.shape)

# one-hot编码
# 看了print出来的结果后就明白这里为啥用one-hot编码了(看一下打印的结果，下面这篇文章挺多人觉得好，所以就展示出来了)
# 而且对于神经网络处理分类问题，都要将目标值(也就是分类的每个类别)变成one-hot编码 ==> https://blog.csdn.net/nini_coded/article/details/79250600
y_train = tf.one_hot(y_train, depth=10)
print("one-hot编码后\n", y_train)

# 构建数据集对象(这里更应该说是加载数据集)  ==》五步加载数据集： https://blog.csdn.net/rainweic/article/details/95737315
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test))
# 批量训练
train_dataset = train_dataset.batch(200)       # 将train_dataset中的60000个数据分成300份，每份200个样本

model = keras.Sequential([
    keras.layers.Dense(units=512, activation='relu'),                                      # https://blog.csdn.net/weixin_42499236/article/details/84624195
    keras.layers.Dense(units=256, activation='relu'),
    keras.layers.Dense(units=10)
])


# 进行训练优化权重的函数
def train_epoch(epoch):
    # step4
    for step, (x, y) in enumerate(train_dataset):    # 这里会循环300次，每次喂进去200个样本，数据总量是60000=200*300
        # 构建梯度记录环境   在with后面写入要被梯度下降的函数方程  https://blog.csdn.net/xierhacker/article/details/53174558
        with tf.GradientTape() as tape:                         #
            # [b, 28, 28] => [b, 10]   b应该是每次投喂的样本数量，这里应该是200
            x = tf.reshape(x, (-1, 28*28))        # 在进入神经网络之前，我们要将数据flatten一下，这样每个像素点特征就
            # 得到模型的输出结果 output [b, 28*28]==>[b, 10]
            print("----------------", step)
            out = model(x)
            # 计算每个样本的平均误差， x.shape[0] ==》 [b]样本数量
            # reduce_sum() 用于计算张量tensor沿着某一维度的和，可以在求和后降维。
            # tf.square求内部平方值
            loss = tf.reduce_sum(tf.square(out - y)) / x.shape[0]

        # 梯度下降优化model中的每个权值  optimize and update w1, w2, w3, b1, b2, b3
        # 先计算参数的梯度
        grads = tape.gradient(loss, model.trainable_variables)         # 感觉这个函数就是求导用的，求出每个特征值得导数
        # 梯度下降中的优化器
        optimizer = keras.optimizers.SGD(learning_rate=0.001)
        # 将计算好的梯度更新到网络中
        optimizer.apply_gradients(zip(grads, model.trainable_variables)) # 这一步将得到的方向导数，更新到每一个权重上

    return loss.numpy()

# 主函数
def train():
    loss_list = list()

    # 进行多次训练
    for epoch in range(15):
        loss = train_epoch(epoch)
        loss_list.append(loss)
        print(epoch,"===========>" ,loss)

    x = [i for i in range(15)]
    plt.plot(x, loss_list, color="yellow", marker="s", label="训练误差")
    plt.xlabel("Epoch")
    plt.ylabel("MSE")
    plt.savefig("MNIST数据集训练误差.png")
    plt.show("哈哈")


if __name__=="__main__":
    train()



