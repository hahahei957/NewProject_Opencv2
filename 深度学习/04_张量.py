import tensorflow as tf

"""
很重要：
https://blog.csdn.net/l7H9JA4/article/details/92857163?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1
"""

# 类似于python的编程形式，除去了过去构图加会话，更加简洁、方便debug
def test1():
    random_value = tf.random.uniform([], 0, 1)
    x = tf.reshape(tf.range(0, 4), [2, 2])
    print(random_value)
    if random_value.numpy() > 0.5:
        y = tf.matmul(x, x)
        print("11111111111")
        print(f"x:{x}")
        print(f"y:{y}")
    else:
        y = tf.add(x, x)
        print("2222222222")
        print(f"x:{x}")
        print(f"y:{y}")

def test2():
    w = tf.Variable([[2.0]])
    with tf.GradientTape() as tape:
        loss = w * w + 2. * w + 5.
    grad = tape.gradient(loss, w)               # 这个的名字虽然叫计算梯度，但我感觉就是在求导
    print(grad)  # => tf.Tensor([[ 4.]], shape=(1, 1), dtype=float32)

# 此时，输入Tensor的dtype必须是float32，但是shape不限制，当类型不匹配时会出错。
# 还有很多，具体看上面的链接
# 前面说过，python原生的print函数只会在构建Graph时打印一次Tensor句柄。如果想要打印Tensor的具体值，要使用tf.print：

test2()


