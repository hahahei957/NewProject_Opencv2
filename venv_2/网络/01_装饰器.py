
# def set_func(func):
#     def call_func(*args, **kwargs):
#
#         return func()
#
#     return call_func

"""这种做法可以，但是非常的不可取， 如果被修饰的函数带参数， 还要根据被修饰的函数所带的参数多少，在修饰函数中，给func()中的指定位置添加参数"""
def set_func(func):
    def call_func(*args, **kwargs):
        level = args[0]
        if level == 1:
            print("权限 1 即将为您验证")
        elif level == 2:
            print("权限 2 即将为您验证")
        return func()
    return call_func

@set_func
def test1():
    print("__________test1______________")
    return "ok"

@set_func
def test2():
    print("__________test2______________")
    return "ok"

# test1(1)
# test2(2)


"""带参数的修饰器"""
def rounte(level):
    def set_func(func_name):
        def call_funv(*args, **kwargs):
            if level == 1:
                print("权限 1 即将为您验证")
            elif level == 2:
                print("权限 2 即将为您验证")
            return func_name(*args, **kwargs)
        return call_funv
    return set_func


@rounte(1)
def test1():
    print("__________test1______________")
    return "ok"

@rounte(2)
def test2():
    print("__________test2______________")
    return "ok"

test1()
test2()

