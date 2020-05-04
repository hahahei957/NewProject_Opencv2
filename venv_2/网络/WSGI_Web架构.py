
TEMPLATE_ROOT = "./template"
# 方案一
# READY2RUN_DICT = {
#     "/index.py" : index,
#     "/login.py" : login
# }
# 方案二
READY2RUN_DICT = dict()
def url_route(file_name):
    def set_func(funcname):
        """由于我们是在这里将index函数的引用即一坨地址传给了字典READY2RUN_DICT中， 而这里index函数的引用是未被修饰的， 所以字典中存放的函数的引用(一坨地址)是未被修饰的函数地址"""
        READY2RUN_DICT[file_name] = funcname
        def call_func(*args, **kwargs):
            "前面添加的*号是拆包的意思"
            return funcname(*args, **kwargs)
        return call_func
    return set_func

def read_file_info(file_name):
    content = str()                       # 这句话可有可无
    try:
        file_name = file_name.replace('.py', '.html')
        f = open(TEMPLATE_ROOT + file_name, encoding='utf-8')
    except Exception as ret:
        print("访问页面出错啦", ret)
    else:
        content = f.read()
        f.close()
    return content

@url_route("/index.py")
def index(file_name):
    print(1111111111111111111111111111)
    content = read_file_info(file_name)
    return content
    # return "你好，世界！"

@url_route("/login.py")
def login(file_name):
    return "我很好，你呢"

"""http://127.0.0.1:7788/index.py"""

def application(env, response_head_func):
    response_head_func("200 OK", [("Content-Type", "text/html;charset=utf-8")])
    file_name = env["PATH_INFO"]
    # if file_name == "/index.py":
    #     return index()
    # elif file_name == "/login.py":
    #     return login()
    # else:
    #     return "小年快乐！！！！！"

    # func = READY2RUN_DICT[file_name]           # 字典中的value值存放了对函数的引用
    # return func()
    """优先使用try处理异常， 这样可以保证程序不崩溃， 同时可以将前面传递过来的异常处理掉， 保证程序的进行"""
    try:
        return READY2RUN_DICT[file_name](file_name)           # 这里返回的是body的值

    except Exception as ret:
        return "小年快乐， 产生了异常 %s" % str(ret)        # 这里返回的是body的值

