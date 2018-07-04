from flask_admin.contrib.sqla import ModelView
from flask import Blueprint

from flaskshop.extensions import admin_manager, db
from flaskshop.product.models import Product
from flaskshop.order.models import Order

blueprint = Blueprint('admin_pannel', __name__, url_prefix='/admin', static_folder='../static')


class CustomView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'


admin_manager.add_view(
    CustomView(Product, db.session, endpoint='Product_admin', menu_icon_type='fa',
               menu_icon_value='fa-circle-o nav-icon'))
admin_manager.add_view(ModelView(Order, db.session, endpoint='Order_admin'))
