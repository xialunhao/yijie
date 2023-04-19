import json
from typing import Union


class HttpRequest:
    def __init__(self, method: str, url: str, headers: dict, params: dict, body: dict, version: str):
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self.body = body
        self.version = version


class HttpResponse:
    def __init__(self, version: str, status_code: int, msg, headers: dict, body: Union[dict, str]):
        self.version = version
        self.status_code = status_code
        self.msg = msg
        self.headers = headers
        self.body = body


def handle_http_warp(content: str) -> HttpRequest:
    content = content.replace('\r', '')
    header_content, body_content = content.split("\n\n")[0], content.split("\n\n")[1]
    headers_content_list = header_content.split("\n")

    # 处理method
    http_info = headers_content_list[0].split(" ")
    method = http_info[0]
    url = http_info[1].split("?")[0]
    http_version = http_info[2]

    # 处理params
    total_url = http_info[1]
    params = {}
    if "?" in total_url and not total_url.endswith("?"):
        params_content = total_url.split("?")[1]
        if "&" in params_content:
            params_content_list = params_content.split("&")
            for param in params_content_list:
                key, value = param.split("=")[0], param.split("=")[1]
                params[key] = value
        else:
            key, value = params_content.split("=")[0], params_content.split("=")[1]
            params[key] = value

    # 处理headers
    headers = {}
    for header in headers_content_list[1:]:
        header = header.replace(' ', '')
        key, value = header.split(':')[0], header.split(':')[1]
        headers[key] = value

    # 处理body
    try:
        bodys = json.loads(body_content.replace('\n', '').replace(' ', ''))
    except:
        bodys = {}

    # 构造函数
    http_warp = HttpRequest(method=method, url=url, headers=headers, params=params, body=bodys, version=http_version)
    return http_warp


def create_http_warp(http_warp: HttpResponse) -> str:
    version = http_warp.version
    status_code = http_warp.status_code
    msg = http_warp.msg
    headers = http_warp.headers
    body = http_warp.body

    # 构建一个content
    content = f"{version} {status_code} {msg}\r\n"
    for k, v in headers.items():
        content += f"{k}: {v}\r\n"
    content += "\r\n"
    try:
        content += json.dumps(body)
    except:
        pass
    return content

