import functools

from flask import json, Flask
from werkzeug.wrappers import Response


class ApiResult:
    def __init__(self, data, status=200):
        self.data = data
        self.status = status

    def to_response(self):
        if "r" not in self.data:
            self.data["r"] = 0
        return Response(
            json.dumps(self.data), mimetype="application/json", status=self.status
        )


class ApiFlask(Flask):
    def make_response(self, receive):
        if isinstance(receive, Response):
            return receive

        if isinstance(receive, (dict, list)):
            data = {"data": receive}
            receive = ApiResult(data)
        if isinstance(receive, ApiResult):
            return receive.to_response()

        return Flask.make_response(self, receive)


def marshal(data, schema):
    if isinstance(data, (list, tuple)):
        return filter(None, [marshal(d, schema) for d in data])

    result, errors = schema.dump(data)
    if errors:
        for item in errors.items():
            print("{}: {}".format(*item))
    return result


class marshal_with:
    def __init__(self, schema_cls):
        self.schema = schema_cls()

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            resp = fn(*args, **kwargs)
            return marshal(resp, self.schema)

        return wrapper


# the view func is partital, add wrapper to make it has __name__
def wrap_partial(fn, *args, **kwargs):
    partial_func = functools.partial(fn, *args, **kwargs)
    functools.update_wrapper(partial_func, args[0])
    return partial_func
