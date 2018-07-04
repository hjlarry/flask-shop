from flask_admin.contrib.sqla import ModelView
from flask import Blueprint

from flaskshop.extensions import admin_manager, db
from flaskshop.product.models import Product
from flaskshop.order.models import Order

blueprint = Blueprint('admin_pannel', __name__, url_prefix='/admin', static_folder='../static')


class ProductView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'
    column_list = ('id', 'title', 'image', 'on_sale', 'rating', 'sold_count', 'review_count', 'price')
    can_delete = False


admin_manager.add_view(
    ProductView(Product, db.session, endpoint='Product_admin', menu_icon_type='fa',
                menu_icon_value='fa-bandcamp nav-icon'))
admin_manager.add_view(ModelView(Order, db.session, endpoint='Order_admin', menu_icon_type='fa',
                                 menu_icon_value='fa-cart-arrow-down nav-icon'))
