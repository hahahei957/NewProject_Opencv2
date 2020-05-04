import tensorflow as tf
import os

tf.compat.v1.disable_eager_execution()

def demo_1():
    a = 1
    b = 2
    c = tf.constant(3)
    sum1 = a+b
    sum2 = tf.add(a, c)
    sum3 = b + c

    with tf.compat.v1.Session() as sess:
        # 有重载的机制,默认会给运算符重载成op类型
        print(f"sum2:{sum2.eval()}")       # eval默认就是执行该节点，并返回该节点储存的数据
        print(f"sum2:{sum3.eval()}")

def demo_2():
    # placeholder是一个占位符,feed_dict一个字典,具体解释请看 ==》 https://blog.csdn.net/Ftwhale/article/details/104854687?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1
    plt = tf.compat.v1.placeholder(dtype=tf.float16, shape=((3, 3)))
    print(plt)
    with tf.compat.v1.Session() as sess:
        # 执行placeholder时，要给其传入值
        print(sess.run(plt, feed_dict={plt: [[1, 2, 3], [4, 5, 36], [2, 3, 4]]}))

# 形状的概念
# 动态形状和numpy.reshape差不多
# 静态形状：一旦张量的形状固定了。就不能再次给其设置形状
# 而是通过动态形状产生一个新的形状传出来，给别人，但原本的张量是无法改变的
def test_3():
    plt = tf.compat.v1.placeholder(tf.float32, [None, 2])
    # plt.set_shape([3, 2])               # 这个是设置静态形状，一旦确定为3，2就无法通过静态设置来更改维度， 但可以通过reshape动态形状来更改
    print(plt)
    plt_reshape = tf.reshape(plt, [3, 4])
    print(plt_reshape)

# 变量op
# 1、变量op能够持久化保存，普通张量op是不行的
# 2、当定义一个变量op的时候，一定要在会话当中去运行初始化
# 3、name参数：在tensorboard使用的时候显示名字，可以让相同op名字的进行区分
def test_4():
    a = tf.constant(3.0)
    var = tf.Variable(tf.random_normal_initializer([2, 3], mean=0.0, stddev=1.0))
    print(a, var)

    # 必须进行一部显示的初始化便变量op

# demo_2()
test_3()
