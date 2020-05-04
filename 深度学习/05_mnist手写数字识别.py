import tensorflow as tf


class Network:
    def __init__(self):
        # 学习率，一般在 .000001-0.5之间
        self.learning_rate = 0.001

        # 输入张量 28 * 28 = 784个像素的图片一维向量
        self.x = tf.placeholder(tf.float32, [None, 784])

        # 标签值，即图像对应的结果，如果对应数字是8，则对应label是 [0,0,0,0,0,0,0,0,1,0]
        # 这种方式称为 one-hot编码
        # 标签是一个长度为10的一维向量，值最大的下标即图片上写的数字
        self.label = tf.placeholder(tf.float32, [None, 10])

        # 初始化权重，这里初始化为0,因为权重是要一直改变校正的，所以定义为一个变量值
        self.w = tf.Variable(tf.zeros([784, 10]))        # 784个像素点(特征值),对应10个输出结果(0-9)
        # 初始化偏置(就是y=wx+b中的b
        self.bias = tf.Variable(tf.zeros([10]))
        # 输出 y = softmax(X * w + b)
        self.y = tf.nn.softmax(tf.matmul(self.x, self.w) + self.bias)

        # 损失熵，即交叉熵
        self.lose = tf.reduce_sum(self.label*tf.log(self.y+1e-10))               # 用于计算张量tensor沿着某一维度的和,可以在求和后降维。

