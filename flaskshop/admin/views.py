import ast
from flask import Blueprint, flash, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import form, actions
from flask_login import current_user
from jinja2 import Markup
from wtforms.fields import (
    IntegerField,
    BooleanField,
    DecimalField,
    PasswordField,
    TextField,
    SelectField,
)
from wtforms.validators import Email, DataRequired

from flaskshop.extensions import admin_manager, db, csrf_protect
from flaskshop.constant import *
from flaskshop.settings import Config
from flaskshop.product.models import Product
from flaskshop.order.models import Order, OrderItem
from flaskshop.account.models import User
from flaskshop.checkout.models import CouponCode
from .utils import MultipleImageUploadField, CKTextAreaField

blueprint = Blueprint("admin_pannel", __name__, url_prefix="/admin")


class CustomView(ModelView):
    list_template = "admin/list.html"
    create_template = "admin/create.html"
    edit_template = "admin/edit.html"
    can_delete = True
    can_export = True
    can_set_page_size = True

    form_widget_args = {"created_at": {"disabled": True}}

    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_admin:
            flash('This is not an administrator', 'warning')
            return False
        if current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('public.login', next=request.url))


class ProductView(CustomView):
    column_list = (
        "id",
        "title",
        "image",
        "on_sale",
        "rating",
        "sold_count",
        "review_count",
        "price",
    )
    column_sortable_list = (
        "id",
        "title",
        "rating",
        "sold_count",
        "review_count",
        "price",
    )
    column_editable_list = ('title', 'rating')
    column_filters = ('id', 'title')
    product_sku_options = {
        "form_excluded_columns": ("created_at",),
        "form_overrides": dict(description=TextField),
    }
    # inline_models = [(ProductSku, product_sku_options)]
    extra_js = ["//cdn.ckeditor.com/4.6.0/standard/ckeditor.js"]
    form_excluded_columns = ("liked_users",)
    form_extra_fields = {
        "image": MultipleImageUploadField('Image', base_path=Config.STATIC_DIR, thumbnail_size=(200, 100, True),
                                          relative_path='images/'),
        "on_sale": BooleanField(),
        "sold_count": IntegerField(),
        "review_count": IntegerField(),
        "rating": DecimalField(),
        "price": DecimalField(),

    }
    form_overrides = {"description": CKTextAreaField}

    def __init__(self):
        super().__init__(
            Product,
            db.session,
            endpoint="product_admin",
            menu_icon_value="fa-bandcamp nav-icon",
        )

    def _format_price(view, context, model, name):
        return Markup("￥{}".format(model.price))

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        elif model.image.startswith('http'):
            url = model.image
        else:
            url = url_for('static', filename=form.thumbgen_filename(ast.literal_eval(model.image)[0]))
        return Markup("<img src={} width=200 height=100/>".format(url))

    column_formatters = {"price": _format_price, "image": _list_thumbnail}

    @actions.action('on_sale', 'On/Offsale')
    def action_change_on_sale(self, ids):
        try:
            query = Product.query.filter(Product.id.in_(ids))
            for p in query.all():
                p.update(on_sale=not p.on_sale)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
        return


class OrderView(CustomView):
    can_create = False
    column_list = ("id", "no", "user", "total_amount", "paid_at")
    inline_models = (OrderItem,)
    form_excluded_columns = ("user",)
    form_extra_fields = {
        "refund_status": SelectField(
            choices=[
                (REFUND_STATUS_APPLIED, REFUND_STATUS_APPLIED),
                (REFUND_STATUS_FAILED, REFUND_STATUS_FAILED),
                (REFUND_STATUS_PENDING, REFUND_STATUS_PENDING),
                (REFUND_STATUS_PROCESSING, REFUND_STATUS_PROCESSING),
                (REFUND_STATUS_SUCCESS, REFUND_STATUS_SUCCESS),
            ]
        ),
        "ship_status": SelectField(
            choices=[
                (SHIP_STATUS_DELIVERED, SHIP_STATUS_DELIVERED),
                (SHIP_STATUS_PENDING, SHIP_STATUS_PENDING),
                (SHIP_STATUS_RECEIVED, SHIP_STATUS_RECEIVED),
            ]
        ),
    }

    def __init__(self):
        super().__init__(
            Order,
            db.session,
            endpoint="order_admin",
            menu_icon_value="fa-cart-arrow-down nav-icon",
        )

    def _format_price(view, context, model, name):
        return Markup("￥{}".format(model.total_amount))

    column_formatters = {"total_amount": _format_price}


class CouponView(CustomView):
    column_list = (
        "id",
        "title",
        "type",
        "enabled",
        "value",
        "min_amount",
        "used_total",
    )
    form_excluded_columns = ("order",)
    form_extra_fields = {
        "type": SelectField(
            choices=[(TYPE_FIXED, TYPE_FIXED), (TYPE_PERCENT, TYPE_PERCENT)]
        )
    }
    form_args = {
        'not_before': {'label': 'Start Time'},
        'not_after': {'label': 'End Time'},
    }

    def __init__(self):
        super().__init__(
            CouponCode,
            db.session,
            endpoint="coupon_admin",
            menu_icon_value="fa-bitcoin nav-icon",
        )

    def _format_used_total(view, context, model, name):
        html = """
        <div class="progress">
          <div class="progress-bar" role="progressbar" style="width:{width}%">
            {used}/{total}
          </div>
        </div>
        """

        return Markup(html.format(used=model.used, total=model.total, width=model.used / model.total * 100))

    column_formatters = {"used_total": _format_used_total}


class UserView(CustomView):
    column_list = ("id", "username", "email", "active", "is_admin")
    form_excluded_columns = (
        "orders",
        "favor_products",
        "addresses",
        "cart_items",
        "password",
    )
    form_args = dict(email=dict(validators=[Email(), DataRequired()]))
    form_extra_fields = {"this_password": PasswordField("Password")}

    def __init__(self):
        super().__init__(
            User,
            db.session,
            endpoint="user_admin",
            menu_icon_value="fa-user nav-icon",
        )

    def on_model_change(self, form, User, is_created):
        if form.this_password.data:
            User.set_password(form.this_password.data)


csrf_protect.exempt(CustomView.ajax_update)
admin_manager.add_views(ProductView(), OrderView(), CouponView(), UserView())
