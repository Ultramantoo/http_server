import socket
import re
import gevent
from gevent import monkey

monkey.patch_all()

def service_client(new_socket):
    """为这个客户端返回数据"""
    # 1.接收浏览器发送过来请求，即Http请求
    request = new_socket.recv(1024).decode()
    # print(request)
    request_lines = request.splitlines()
    # print(request_lines[0])

    request_page = re.findall(" (.+) HTTP/1.1",request_lines[0])[0]
    # print(request_page)
    if request_page =="/": request_page="/index.html"
    request_page = request_page[1:]
    print(request_page)


    try:
        with open(r".\html\\" + request_page, "rb") as f:
            html_content = f.read()
    except:
        # 无法访问的页面时
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "------file not found------"
        html_content = response.encode("utf-8")
    else:
        # 2.返回ht格式的数据，给浏览器
        # 2.1准备发送给浏览器的数据--header
        response = "HTTP/1.1 200 OK\r\n"
        response += "\r\n"
        # 2.2 准备发送给浏览器的数据---boy
        # response += "hahahaha, hello"
        new_socket.send(response.encode("utf-8"))

    new_socket.send(html_content)

    # 3.关闭套接字
    new_socket.close()


def main():
    """用来完成整体的控制"""
    # 1. 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定
    tcp_server_socket.bind(("", 7891))

    # 3. 变为监听套接字
    tcp_server_socket.listen(128)

    while True:
        # 4. 等待新客户端链接
        new_socket, client_addr = tcp_server_socket.accept()

        # 5. 为这个客户端服务
        # service_client(new_socket)
        gevent.spawn(service_client,new_socket)

        # new_socket.close()

        # break

    # 关闭监听套接字
    tcp_server_socket.close()


if __name__ == "__main__":
    main()
