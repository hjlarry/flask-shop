from flask_admin.contrib.sqla import ModelView
from flask import Blueprint
from jinja2 import Markup
from wtforms.fields import IntegerField, BooleanField, DecimalField, TextAreaField
from wtforms.widgets import TextArea

from flaskshop.extensions import admin_manager, db
from flaskshop.product.models import Product, ProductSku
from flaskshop.order.models import Order
from flaskshop.user.models import User
from flaskshop.cart.models import CouponCode

blueprint = Blueprint('admin_pannel', __name__, url_prefix='/admin', static_folder='../static')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class CustomView(ModelView):
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    can_delete = True
    can_export = True
    can_set_page_size = True


class ProductView(CustomView):
    column_list = ('id', 'title', 'image', 'on_sale', 'rating', 'sold_count', 'review_count', 'price')
    column_sortable_list = ('id', 'title', 'rating', 'sold_count', 'review_count', 'price')
    inline_models = (ProductSku,)
    form_excluded_columns = ('liked_users',)
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    # column_editable_list = ('title', 'rating') //TODO
    # column_filters = ('id', 'title') //TODO
    def _format_price(view, context, model, name):
        return Markup("￥{}".format(model.price))

    def _list_thumbnail(view, context, model, name):
        return Markup("<img src={} width=200 height=100/>".format(model.image))

    column_formatters = {
        'price': _format_price,
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'on_sale': BooleanField(),
        'sold_count': IntegerField(),
        'review_count': IntegerField(),
        'rating': DecimalField(),
        'price': DecimalField()
    }

    form_overrides = {
        'description': CKTextAreaField
    }


class UserAddressView(CustomView):
    can_delete = False


product_view = ProductView(Product, db.session, endpoint='Product_admin',
                           menu_icon_type='fa', menu_icon_value='fa-bandcamp nav-icon')
order_view = CustomView(Order, db.session, endpoint='Order_admin',
                        menu_icon_type='fa', menu_icon_value='fa-cart-arrow-down nav-icon')
coupon_view = CustomView(CouponCode, db.session, endpoint='Coupon_admin',
                         menu_icon_type='fa', menu_icon_value='fa-bitcoin nav-icon')
user_view = CustomView(User, db.session, endpoint='User_admin',
                       menu_icon_type='fa', menu_icon_value='fa-user nav-icon')

admin_manager.add_view(product_view)
admin_manager.add_view(order_view)
admin_manager.add_view(coupon_view)
admin_manager.add_view(user_view)
