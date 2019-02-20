from functools import wraps
from flask import Blueprint, render_template, abort, redirect
from flask_login import login_required, current_user

from flaskshop.dashboard.models import DashboardMenu
from .user import users, user, user_edit, address_edit
from .site import (
    site_menus,
    site_menus_manage,
    dashboard_menus,
    dashboard_menus_manage,
    site_pages,
    site_pages_manage,
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
from flaskshop.settings import Config

template_folder = Config.APP_DIR / "templates" / "dashboard" / "adminlte"
blueprint = Blueprint(
    "dashboard", __name__, url_prefix="/dashboard", template_folder=template_folder
)


@blueprint.context_processor
def inject_param():
    menus = DashboardMenu.first_level_items()
    return {"menus": menus}


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


@blueprint.before_request
@admin_required
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
blueprint.add_url_rule("/users", view_func=users)
blueprint.add_url_rule("/users/<user_id>", view_func=user)
blueprint.add_url_rule(
    "/users/<user_id>/edit", view_func=user_edit, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/address/<id>/edit", view_func=address_edit, methods=["GET", "POST"]
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
blueprint.add_url_rule("/product/<id>", view_func=product_detail)
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
    "/variant/create", view_func=variant_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/variant/<id>/edit", view_func=variant_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule("/orders", view_func=orders)
blueprint.add_url_rule("/order/<id>", view_func=order_detail)
