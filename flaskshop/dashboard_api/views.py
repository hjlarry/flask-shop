from functools import partial

from flaskshop.account.models import User
from flaskshop.product.models import (
    ProductType,
    Category,
    Collection,
    ProductAttribute,
    Product,
    ProductVariant,
)
from flaskshop.discount.models import Sale
from flaskshop.dashboard.models import DashboardMenu

from .utils import ApiResult


def user_del(id):
    try:
        user = User.get_by_id(id)
        user.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def product_type_del(id):
    try:
        product_type = ProductType.get_by_id(id)
        product_type.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def category_del(id):
    try:
        category = Category.get_by_id(id)
        category.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def collection_del(id):
    try:
        collection = Collection.get_by_id(id)
        collection.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def attribute_del(id):
    try:
        attr = ProductAttribute.get_by_id(id)
        attr.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def variant_del(id):
    try:
        variant = ProductVariant.get_by_id(id)
        variant.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def product_del(id):
    try:
        product = Product.get_by_id(id)
        product.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())


def item_del(cls, id):
    try:
        item = cls.get_by_id(id)
        item.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())

sale_del = partial(item_del, cls=Sale)
sale_del.__name__ = "sale_del"

dashboard_menu_del = partial(item_del, cls=DashboardMenu)
dashboard_menu_del.__name__ = "dashboard_menu_del"