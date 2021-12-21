import enum

from .utils import ApiResult


class ApiException(Exception):
    def __init__(self, error, real_message=None):
        self.code, self.message, self.status = error
        if real_message is not None:
            self.message = real_message

    def to_result(self):
        return ApiResult(
            {"errmsg": self.message, "r": self.code, "status": self.status}
        )


class httperrors(enum.Enum):
    unknown_error = (1000, "unknown error", 400)
    access_forbidden = (1001, "access forbidden", 403)
    unimplemented_error = (1002, "unimplemented error", 400)
    not_found = (1003, "not found", 404)
    illegal_state = (1004, "illegal state", 400)
    not_supported = (1005, "暂时不支持此操作", 400)
    post_not_found = (1006, "Post不存在", 400)
