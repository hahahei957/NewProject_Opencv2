import tensorflow as tf
import os
# 创建一张图包含了一组op和tensor,上下文环境
# op:只要使用tensorflow的API定义的函数都是OP
# tensor：就指代的是数据  ==  数组的形式
"""NumPy数组和tf.Tensors之间最明显的区别是：
张量可以由加速器内存（如GPU，TPU）支持。
张量是不可变的。"""

# https://www.cnblogs.com/123456www/p/12584427.html
tf.compat.v1.disable_eager_execution()          # 强制让v2.0兼容v1.0（它可以用于从TensorFlow 1.x到2.x的复杂迁移项目的程序开头。）
# Sess = tf.compat.v1.Session()

a = tf.constant(2)
b = tf.constant(5)

sum1 = tf.add(a, b)

# 下面这种格式不常用
print(f"sum1:{sum1}")
# with Sess.as_default():            # 关于as_default() ==》 as_default()
#     session = Sess
#     session.run(sum1)
#     print(sum1.eval())
#     session.close()

with tf.compat.v1.Session() as sess:        # 升级到2.0之后，会话模块就没了。。。只能通过这个来迁移函数
    sess.run(sum1)
    print(sum1.eval())               # 表示直接执行这个节点，打印出来这个节点的数值




