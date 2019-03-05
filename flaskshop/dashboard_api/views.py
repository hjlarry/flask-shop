from flaskshop.account.models import User
from flaskshop.product.models import ProductType, Category, Collection, ProductAttribute

from .utils import ApiResult


def user_del(id):
    try:
        user = User.get_by_id(id)
        user.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": e.message})
    return ApiResult(dict())


def product_type_del(id):
    try:
        product_type = ProductType.get_by_id(id)
        product_type.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": e.message})
    return ApiResult(dict())


def category_del(id):
    try:
        category = Category.get_by_id(id)
        category.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": e.message})
    return ApiResult(dict())


def collection_del(id):
    try:
        collection = Collection.get_by_id(id)
        collection.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": e.message})
    return ApiResult(dict())


def attribute_del(id):
    try:
        attr = ProductAttribute.get_by_id(id)
        attr.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": e.message})
    return ApiResult(dict())
