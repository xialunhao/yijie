# -*- coding: utf-8 -*-
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM

from .common import HttpResponse, HttpRequest, create_http_warp, handle_http_warp
from .router import router


def handle_request(http_request: HttpRequest) -> HttpResponse:
    method = http_request.method
    url = http_request.url
    func = router.get(method, {}).get(url)
    if not func:
        http_response = HttpResponse(version=http_request.version, status_code=404, msg="Not Found",
                                     headers={"Content-Type": "text/plain; charset=utf-8"}, body="404 Not Found")
    else:
        body = func(http_request)
        http_response = HttpResponse(version=http_request.version, status_code=200, msg="OK",
                                     headers={"Content-Type": "application/json"}, body=body)
    return http_response


def handle_conn(sock_client):
    request_content = b''
    while True:
        data = sock_client.recv(1024)
        request_content += data
        # 判断请求数据是否已经接收完成
        if b'\r\n\r\n' in request_content:
            header, body = request_content.split(b'\r\n\r\n', 1)
            # 解析请求头中的 Content-Length 字段
            content_length = 0
            for line in header.split(b'\r\n'):
                if line.startswith(b'Content-Length:'):
                    content_length = int(line.split(b':', 1)[1].strip())
                    break
            # 判断请求数据是否已经完整接收
            if len(body) >= content_length:
                break
    # print(f"Got: \n{request_content.decode('utf-8')}")
    # 将二进制专户为http request的对象
    http_request = handle_http_warp(request_content.decode('utf-8'))
    # 处理request
    http_response = handle_request(http_request)
    # 将生成的 http response包转化为二进制
    response_content = create_http_warp(http_response).encode()
    # 返回数据
    sock_client.sendall(response_content)
    # 响应结束，返回包
    sock_client.close()


def start_server(host="localhost", port=5000, back_log=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(back_log)
    print(f"start server in host:{host}, port:{port}")

    type = 1
    if type == 1:
        # 起一个线程池
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                sock_client, address = sock.accept()
                executor.submit(handle_conn, sock_client)

    if type == 2:
        # 使用多线程来做
        while True:
            sock_client, address = sock.accept()
            # handle_conn(sock_client, address)
            t = threading.Thread(target=handle_conn, args=(sock_client,))
            t.start()

    if type == 3:
        # 什么都不用，单进程来跑
        while True:
            sock_client, address = sock.accept()
            handle_conn(sock_client)

    # 这边基本上是不太可能的，因为同一个端口无法回复
    if type == 4:
        # 起一个线程池
        with ProcessPoolExecutor(max_workers=10) as executor:
            while True:
                sock_client, address = sock.accept()
                executor.submit(handle_conn, sock_client)
