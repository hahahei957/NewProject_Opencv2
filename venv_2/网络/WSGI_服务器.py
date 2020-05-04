import socket
import multiprocessing
import re
import WSGI_Web架构 as subroutine


class WSGIServer(object):
    def __init__(self, port, documents_root):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定地址
        self.server_socket.bind(("", port))
        # 这里直接将端口号变量装进了元祖中， 不知道可不可以
        # server_socket.setsockopt(socket.SOLSOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # print("_______________1__________________")
        # self.server_socket.listen(128)

        self.documents_root = documents_root

    def handle_client(self, client_socket):
        try:
            recv_data = client_socket.recv(1024 * 1024).decode("utf-8")
        except Exception as ret:
            print("=========>", ret)
            return

            # 判断浏览器是否关闭了   ！！！！！！！！！！！！！！！！！！！！！1
        # 通过判断浏览器是否关闭了，直接去关闭子进程，应该可能大概会直接避免了三次招手四次挥手

        if recv_data == None:
            return
        # 接收到的信息
        requests_lines = recv_data.splitlines()

        print(requests_lines, "************************************")

        # 提取请求的文件(index.html)
        # GET /a/b/c/d/e/index.html HTTP/1.1
        try:
            ret = re.match(r"([^/]*)([^ ]+)",requests_lines[0])                  # 不知道为啥，requests_lines传回来的值，有的时候是空值
        except:
            response_head = "http/1.1 404 file not found\r\n"
            response_head += "\r\n"
            response_body = "requests_lines是空的"
            response_thing = response_head+response_body
            client_socket.send(response_thing.encode("utf-8"))
            return                                                               # 因为这个是子进程，所以哪里出错了，直接return把子进程关掉即可，只要保证主服务器别挂掉就行

        file_name = None
        # 取出客户端索取的信息
        if ret:
            print(ret.group(1), "————————————————————————0——————————")
            print(ret.group(2), "_______________1__________________")
            if ret.group(2) == "/":
                file_name = "/index.html"
            else:
                file_name = ret.group(2)

        # 如果用户请求的是静态内容则直接返回， 如果是动态内容则通过WSGI框架进行逻辑处理
        if not file_name.endswith(".py"):
            try:
                f = open(self.documents_root + file_name, "rb")
            except:
                response_body = "file not found, please input the right url"

                response_head = "http/1.1 404 not found\r\n"
                response_head += "Content-Type: text/html; charset=utf-8\r\n"
                response_head += "Content-Length: %d\r\n" % (len(response_body))
                response_head += "\r\n"
                response_thing = response_head.encode("utf-8") + response_body.encode("utf-8")  # 这句和else中的那一句话不一样，注意区分开
                client_socket.send(response_thing)
            else:
                content = f.read()
                f.close()
                response_head = "http/1.1 200 OK\r\n"
                response_head += "\r\n"
                response_body = content

                # 因为对于body的内容二进制的形式， 而head是我们输入的
                response_thing = response_head.encode("utf-8") + response_body
                client_socket.send(response_thing)

            # 当客户端索取的文件是以.py结尾的，则用户要动态资源，则通过else来实现
        else:
            # if file_name =="/login.py":
            #     pass

            # 字典env用于传递给web框架。传递给其所需要的数据
            env = dict()
            env["PATH_INFO"] = file_name
            response_body = subroutine.application(env, self.dealing_response_head)
            response_head = "http/1.1 %s\r\n" % self.status
            for info in self.heads:
                response_head += "%s: %s\r\n" % (info[0], info[1])
            response_head += "\r\n"
            response_thing = response_head + response_body
            print("***********************")
            client_socket.send(response_thing.encode("utf-8"))

    # 咋这个函数中。 根据需要我们也初始化了两个变量，从而方便传给hand_client，方便其对以.py结尾的文件进行处理
    def dealing_response_head(self, status, response_head_env):
        self.status = status
        self.heads = [("server_name", "mine_web 1.0")]
        self.heads += response_head_env  # response_head_env是从mine_web架构中传来的head信息

        # 返回信息00
        # 表头信息
        response_head = "HTTP/1.1 200 OK\r\n"  # \r\n都是换行符，通过\r\n就可以实现换行
        response_head += "\r\n"

    def run_forver(self):
        print("_______________1__________________")
        self.server_socket.listen(128)
        while True:
            # 设置为监听

            print("________________2______________")

            new_client, new_client_addr = self.server_socket.accept()
            print("________________3_________________")

            self.handle_client(new_client)
            new_client.close()
            # 在我们调用子套接字通信结束的命令，三次握手四次挥手开始，此时我们并没有与new_client断开联系,
            # 从而导致在 server_socket.accept()这里并没有发生堵塞
            # 而是正式发起了三次握手四次挥手，我们回送内容的body如果是input，让服务器输入发送内容好几次
            # 而链接我们的客户端，并未显示我们的Input,因为这是三次握手和四次挥手的内容


def main():
    httpd = WSGIServer(7788, "./")
    httpd.run_forver()


if __name__ == "__main__":
    main()