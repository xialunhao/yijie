router = {
    "GET": {},
    "POST": {}
}


def register_router(url: str, methods: list):
    def func3(func):
        if not all([method in ["GET", "POST", "DELETE", "OPTIONS", "PUT", "HEAD"] for method in methods]):
            print(f"链接【{url}】的方法【{methods}】设置错误。")
        for method in methods:
            router[method][url] = func
        return func

    return func3
