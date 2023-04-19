一个简单的示例

```
from yijie import start_server
from yijie.common import HttpRequest
from yijie.router import register_router


@register_router(url="/ping", methods=['GET', 'POST'])
def pong(http_request: HttpRequest):
    return {"code": 0, "msg": "success", "result": "pong!"}


if __name__ == "__main__":
    start_server(host="0.0.0.0", port=5000)

```