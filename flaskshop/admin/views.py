from flask import Blueprint

from flaskshop.extensions import admin_manager, csrf_protect
from .product_view import ProductView, ProductImageView
from .order_view import OrderView
from .user_view import UserView

from .utils import CustomView

blueprint = Blueprint("admin_pannel", __name__, url_prefix="/admin")

csrf_protect.exempt(CustomView.ajax_update)
admin_manager.add_views(UserView(), ProductView(), OrderView(), ProductImageView())
