import datetime
import time

from yijie import start_server
from yijie.common import HttpRequest
from yijie.router import register_router


@register_router(url="/ping", methods=['GET', ])
def pong(http_request: HttpRequest):
    print(f"start time {datetime.datetime.now()}")
    params = http_request.params
    body = http_request.body

    result = {"get_params": {}, "post_body": {}}
    for k, v in params.items():
        result["get_params"][k] = v
    for k, v in body.items():
        result["post_body"][k] = v
    time.sleep(0.1)
    print(result)
    print(f"end time {datetime.datetime.now()}")
    return result


@register_router(url="/health_check", methods=['GET', 'POST'])
def health_check(http_request: HttpRequest):
    return {"code": 0, "msg": "success"}


if __name__ == "__main__":
    start_server(host="0.0.0.0", port=5000)
