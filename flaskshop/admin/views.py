from flask import Blueprint

from flaskshop.extensions import admin_manager, csrf_protect
from .product_view import ProductView, ProductImageView, ProductVariantView, ProductCategoryView, ProductCollectionView
from .order_view import OrderView, OrderLineView, OrderPaymentView
from .user_view import UserView, UserAddressView
from .discount_view import SaleView, VoucherView
from .site_view import SiteView, MenuItemView, PageView, ProductTypeView, ProductAttributeView

from .utils import CustomView

blueprint = Blueprint("admin_pannel", __name__, url_prefix="/admin")

csrf_protect.exempt(CustomView.ajax_update)
admin_manager.add_views(UserView(), UserAddressView(), ProductView(), ProductCategoryView(),
                        ProductCollectionView(), ProductImageView(), ProductVariantView(), OrderView(), OrderLineView(),
                        OrderPaymentView(), SaleView(), VoucherView(), SiteView(), MenuItemView(), PageView(),
                        ProductTypeView(), ProductAttributeView())
