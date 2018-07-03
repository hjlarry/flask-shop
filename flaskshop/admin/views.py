from flask_admin.contrib.sqla import ModelView
from flask import Blueprint

from flaskshop.extensions import admin_manager, db
from flaskshop.product.models import Product
from flaskshop.order.models import Order

blueprint = Blueprint('admin_pannel', __name__, url_prefix='/admin', static_folder='../static')

admin_manager.add_view(ModelView(Product, db.session, endpoint='Product_admin'))
admin_manager.add_view(ModelView(Order, db.session, endpoint='Order_admin'))
