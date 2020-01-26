from functools import wraps
from flask import Blueprint, render_template, abort, redirect
from flask_login import login_required, current_user

from flaskshop.dashboard.models import DashboardMenu
from flaskshop.account.utils import permission_required
from flaskshop.settings import Config
from flaskshop.constant import Permission
from .user import users, user, user_edit, address_edit
from .site import (
    site_menus,
    site_menus_manage,
    dashboard_menus,
    dashboard_menus_manage,
    site_pages,
    site_pages_manage,
    site_config,
)
from .product import (
    attributes,
    attribute_manage,
    collections,
    collection_manage,
    categories,
    category_manage,
    product_types,
    product_type_manage,
    products,
    product_detail,
    product_edit,
    product_create_step1,
    product_create_step2,
    variant_manage,
)
from .order import orders, order_detail
from .discount import vouchers, voucher_manage, sales, sale_manage


blueprint = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard",
    template_folder=Config.DASHBOARD_TEMPLATE_FOLDER,
)


@blueprint.context_processor
def inject_param():
    menus = DashboardMenu.first_level_items()
    return {"menus": menus}


@blueprint.before_request
@permission_required(Permission.EDITOR)
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route("/")
def index():
    return render_template("index.html")


blueprint.add_url_rule("/site_menus", view_func=site_menus)
blueprint.add_url_rule(
    "/site_menus/create", view_func=site_menus_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/site_menus/<id>/edit", view_func=site_menus_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/dashboard_menus", view_func=dashboard_menus)
blueprint.add_url_rule(
    "/dashboard_menus/create", view_func=dashboard_menus_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/dashboard_menus/<id>/edit",
    view_func=dashboard_menus_manage,
    methods=["GET", "POST"],
)
blueprint.add_url_rule("/site_pages", view_func=site_pages)
blueprint.add_url_rule(
    "/site_pages/create", view_func=site_pages_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/site_pages/<id>/edit", view_func=site_pages_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/site_config", view_func=site_config, methods=["GET", "POST"])
blueprint.add_url_rule("/users", view_func=users)
blueprint.add_url_rule("/users/<user_id>", view_func=user)
blueprint.add_url_rule(
    "/users/<user_id>/edit", view_func=user_edit, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/users/address/<id>/edit", view_func=address_edit, methods=["GET", "POST"]
)
blueprint.add_url_rule("/attributes", view_func=attributes)
blueprint.add_url_rule(
    "/attributes/create", view_func=attribute_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/attributes/<id>/edit", view_func=attribute_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/collections", view_func=collections)
blueprint.add_url_rule(
    "/collections/create", view_func=collection_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/collections/<id>/edit", view_func=collection_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/categories", view_func=categories)
blueprint.add_url_rule(
    "/categories/create", view_func=category_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/categories/<id>/edit", view_func=category_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/product_types", view_func=product_types)
blueprint.add_url_rule(
    "/product_types/create", view_func=product_type_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/product_types/<id>/edit", view_func=product_type_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/products", view_func=products)
blueprint.add_url_rule("/products/<id>", view_func=product_detail)
blueprint.add_url_rule(
    "/products/create/step1", view_func=product_create_step1, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/products/create/step2", view_func=product_create_step2, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/products/<id>/edit", view_func=product_edit, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/products/variant/create", view_func=variant_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/products/variant/<id>/edit", view_func=variant_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/orders", view_func=orders)
blueprint.add_url_rule("/orders/<id>", view_func=order_detail)
blueprint.add_url_rule("/vouchers", view_func=vouchers)
blueprint.add_url_rule(
    "/vouchers/create", view_func=voucher_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/vouchers/<id>/edit", view_func=voucher_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/sales", view_func=sales)
blueprint.add_url_rule("/sales/create", view_func=sale_manage, methods=["GET", "POST"])
blueprint.add_url_rule(
    "/sales/<id>/edit", view_func=sale_manage, methods=["GET", "POST"]
)
