from flaskshop.account.models import User

from .utils import ApiResult


def user_del(id):
    try:
        user = User.get_by_id(id)
        user.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": e.message})
    return ApiResult(dict())
