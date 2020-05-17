
# MNIST测试实战代码

import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt


# 最简单的预处理函数
def preprocess(x, y):
    '''
    :param x:将numpy转换成Tensor、分类问题还要在这里将label转换为ont-hot编码
    :param y:
    :return:
    '''
    # 转换为
    print(x.shape, y.shape)
    x = tf.cast(x, dtype=tf.float32)/255
    x = tf.reshape(x, [-1, 28*28])
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    print(x.shape, "=======================================")
    print(y.shape, "=======================================")
    return x,y

# 五步法加载数据集
def load_dataset():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    print('x:', x_train.shape, 'y:', y_train.shape, 'x test:', x_test.shape, 'y test:', y_test)
    # Step1 使用 tf.data.Dataset.from_tensor_slices 进行加载
    db_train = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    db_test = tf.data.Dataset.from_tensor_slices((x_test, y_test))

    # Step2 打乱数据
    db_train = db_train.shuffle(1000)
    db_test = db_test.shuffle(1000)

    # Step3 设置batch size：每次投喂进去的数据                           # 这个step3和4这两个步骤貌似不可以颠倒，否则维度会发生变化，但我不知道为啥
    db_train = db_train.batch(512)
    db_test = db_test.batch(512)

    # Step4 使用之前写好的 预处理函数 进行预处理
    # db_train.map(preprocess)
    # 这里map是有返回值的，并不是直接在db_train上修改,不能直接这样db_train.map(preprocess)
    db_train = db_train.map(preprocess)
    db_test = db_test.map(preprocess)

    # Step5 设置迭代次数(迭代2次) test数据集不需要emmm
    db_train = db_train.repeat(20)

    # 随便展示一组数据看看
    x, y = next(iter(db_train))
    print('train sample:', x.shape, y.shape)
    return db_train, db_test

# 设置网络层
def init_parameters():
    # 28*28 => 512             stddev，样本的标准差
    w1, b1 = tf.Variable(tf.random.normal([28*28, 512], stddev=0.1)), tf.Variable(tf.zeros(512))
    # 512 => 256
    w2, b2 = tf.Variable(tf.random.normal([512, 256], stddev=0.1)), tf.Variable(tf.zeros([256]))
    # 256 => 10
    w3, b3 = tf.Variable(tf.random.normal([256, 10], stddev=0.1)), tf.Variable(tf.zeros([10]))

    return w1, b1, w2, b2, w3, b3

# 主训练函数
def train(db_train, db_test, w1, b1, w2, b2, w3, b3, lr=0.01):
    accs, losses = [],[]
    for step, (x_train_many, y_train_many) in enumerate(db_train):
        # TODO：一等把这句删去试试
        x_train_many = tf.reshape(x_train_many, (-1, 28*28))

        # 这篇文章有关于tape的部分 ==》 https://blog.csdn.net/l7H9JA4/article/details/92857163
        # 对于eager执行，每个tape会记录当前所执行的操作，这个tape只对当前计算有效，并计算相应的梯度。PyTorch也是动态图模式，但是与TensorFlow不同，它是每个需要计算Tensor会拥有grad_fn以追踪历史操作的梯度。
        with tf.GradientTape() as tape:
            # layer1
            # print(x_train_many, "----", w1, "----", b1)
            h1 = x_train_many@w1+b1
            h1 = tf.nn.relu(h1)
            # layer2
            h2 = h1@w2+b2
            h2 = tf.nn.relu(h2)
            # 输出层output
            out = h2@w3+b3

            # 损失函数
            loss = tf.reduce_mean(tf.square(y_train_many-out))
        # 在这里运行
        grads = tape.gradient(loss, [w1, b1, w2, b2, w3, b3])
        # 优化更新每个权重和偏执
        for p,g in zip([w1, b1, w2, b2, w3, b3], grads):
            p.assign_sub(lr*g)

        # 每训练80次，打印一下loss函数的优化程度
        if step%80==0:
            print(step, '--loss--', float(loss))
            losses.append(loss)

        # 每循环80次，预测一下测试集，看看拟合效果
        if step%80==0:
            total, total_correct = 0,0
            # 思路：将想x,y乘以前面训练出来的每层网络的权重，得到的预测结果与真实结果进行比对，看看在测试集中的效果
            for x,y in db_test:
                # layer1
                h1 = x@w1+b1
                h1 = tf.nn.relu(h1)
                # layer2
                h2 = h1@w2+b2
                h2 = tf.nn.relu(h2)
                # predict  [b, 10] ==> [b]
                out = h2@w3+b3       # 得到结果是[512, 10]，可以理解为512层数据，每层数据有1行共10个数据， 也就是512个样本，
                # print(out, "================================")
                # convert one-hot y to number y    [512， 10] ==》 [512, ]一维数组
                pred_index = tf.argmax(out, axis=1) # 根据axis取值的不同返回每行或者每列最大值的索引。 ==>  https://blog.csdn.net/u012300744/article/details/81240580
                y_index = tf.argmax(y, axis=1)             # TODO：看看这里打印出来的y的样式
                print(y)
                # bool type  返回的是这512个测试基样本(因为b=512)中每个样本预测正确与否,不在乎这几个类别都是啥，而是在乎这个样本的索引预测与真实值是否一样
                correct = tf.equal(pred_index, y_index)     #
                # 将预测正确的数据进行加和  bool tensor => int tensor => numpy
                total_correct += tf.reduce_sum(tf.cast(correct, dtype=tf.int32)).numpy()
                total += x.shape[0]

            print(step, 'Evaluate Acc:', total_correct/total)
            accs.append(total_correct/total)
    return accs, losses

def main():
    # 加载数据
    db_train, db_test = load_dataset()
    # 获得初始化好的权重和偏置
    w1, b1, w2, b2, w3, b3 = init_parameters()
    # 加入训练函数开始训练
    accs, losses = train(db_train, db_test, w1, b1, w2, b2, w3, b3)

    plt.figure()
    x1 = [i for i in range(len(accs))]
    plt.plot(x1, accs, color='yellow', marker='s')
    x2 = [i for i in range(len(losses))]
    plt.plot(x2, losses, color='green', linestyle='--', marker='s')

    plt.legend(['accs', 'losses'])                    # 设置图例一定要按照这个格式
    plt.savefig('./10_mnist_训练和预测正确率曲线.png')
    plt.show()
    plt.close()


if __name__=="__main__":
    main()
