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

from .utils import ApiResult, wrap_partial


def item_del(cls, id):
    try:
        item = cls.get_by_id(id)
        item.delete()
    except Exception as e:
        return ApiResult({"r": 1, "msg": str(e)})
    return ApiResult(dict())

user_del = wrap_partial(item_del, User)
product_del = wrap_partial(item_del, Product)
variant_del = wrap_partial(item_del, ProductVariant)
collection_del = wrap_partial(item_del, Collection)
category_del = wrap_partial(item_del, Category)
sale_del = wrap_partial(item_del, Sale)
attribute_del = wrap_partial(item_del, ProductAttribute)
product_type_del = wrap_partial(item_del, ProductType)
dashboard_menu_del = wrap_partial(item_del, DashboardMenu)
