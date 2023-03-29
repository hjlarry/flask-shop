from flask import Blueprint
from flask_login import login_required
from pluggy import HookimplMarker

from flaskshop.account.utils import permission_required
from flaskshop.constant import Permission
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.settings import Config

from .index import index
from .discount import (
    sales,
    sales_manage,
    sale_del,
    vouchers,
    vouchers_manage,
    voucher_del,
)
from .order import draft_order, order_detail, orders, send_order
from .product import (
    attributes,
    attributes_manage,
    attribute_del,
    categories,
    categories_manage,
    category_del,
    collections,
    collections_manage,
    collection_del,
    product_create_step1,
    product_detail,
    product_manage,
    product_del,
    product_types,
    product_types_manage,
    product_type_del,
    products,
    variant_manage,
    variant_del,
)
from .site import (
    config_index,
    dashboard_menus,
    dashboard_menus_manage,
    dashboard_menu_del,
    plugin_disable,
    plugin_enable,
    plugin_list,
    shipping_methods,
    shipping_methods_manage,
    shipping_methods_del,
    site_menus,
    site_menus_manage,
    site_menu_del,
    site_pages,
    site_pages_manage,
    site_page_del,
    site_setting,
)
from .user import address_edit, user, user_edit, user_del, users

impl = HookimplMarker("flaskshop")


@impl
def flaskshop_load_blueprints(app):
    bp = Blueprint(
        "dashboard", __name__, template_folder=Config.DASHBOARD_TEMPLATE_FOLDER
    )

    @bp.context_processor
    def inject_param():
        menus = DashboardMenu.first_level_items()
        return {"menus": menus}

    @bp.before_request
    @permission_required(Permission.EDITOR)
    @login_required
    def before_request():
        """The whole blueprint need to login first"""
        pass

    bp.add_url_rule("/", view_func=index)
    bp.add_url_rule("/site_menus", view_func=site_menus)
    bp.add_url_rule(
        "/site_menus/create", view_func=site_menus_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/site_menus/<id>/edit", view_func=site_menus_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/site_menus/<int:id>/delete", view_func=site_menu_del, methods=["DELETE"]
    )
    bp.add_url_rule("/dashboard_menus", view_func=dashboard_menus)
    bp.add_url_rule(
        "/dashboard_menus/create",
        view_func=dashboard_menus_manage,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/dashboard_menus/<id>/edit",
        view_func=dashboard_menus_manage,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/dashboard_menus/<int:id>/delete",
        view_func=dashboard_menu_del,
        methods=["DELETE"],
    )
    bp.add_url_rule("/site_pages", view_func=site_pages)
    bp.add_url_rule(
        "/site_pages/create", view_func=site_pages_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/site_pages/<id>/edit", view_func=site_pages_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/site_pages/<int:id>/delete", view_func=site_page_del, methods=["DELETE"]
    )
    bp.add_url_rule(
        "/site_setting/edit", view_func=site_setting, methods=["GET", "POST"]
    )
    bp.add_url_rule("/plugin", view_func=plugin_list)
    bp.add_url_rule("/plugin/<id>/enable", view_func=plugin_enable, methods=["POST"])
    bp.add_url_rule("/plugin/<id>/disable", view_func=plugin_disable, methods=["POST"])
    bp.add_url_rule("/config", view_func=config_index)
    bp.add_url_rule("/users", view_func=users)
    bp.add_url_rule("/users/<user_id>", view_func=user)
    bp.add_url_rule(
        "/users/<user_id>/edit", view_func=user_edit, methods=["GET", "POST"]
    )
    bp.add_url_rule("/users/<int:id>/delete", view_func=user_del, methods=["DELETE"])
    bp.add_url_rule(
        "/users/address/<id>/edit", view_func=address_edit, methods=["GET", "POST"]
    )
    bp.add_url_rule("/attributes", view_func=attributes)
    bp.add_url_rule(
        "/attributes/create", view_func=attributes_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/attributes/<id>/edit", view_func=attributes_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/attributes/<int:id>/delete", view_func=attribute_del, methods=["DELETE"]
    )
    bp.add_url_rule("/collections", view_func=collections)
    bp.add_url_rule(
        "/collections/create", view_func=collections_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/collections/<id>/edit", view_func=collections_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/collections/<int:id>/delete", view_func=collection_del, methods=["DELETE"]
    )
    bp.add_url_rule("/categories", view_func=categories)
    bp.add_url_rule(
        "/categories/create", view_func=categories_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/categories/<id>/edit", view_func=categories_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/categories/<int:id>/delete", view_func=category_del, methods=["DELETE"]
    )
    bp.add_url_rule("/product_types", view_func=product_types)
    bp.add_url_rule(
        "/product_types/create", view_func=product_types_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/product_types/<id>/edit",
        view_func=product_types_manage,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/product_types/<int:id>/delete", view_func=product_type_del, methods=["DELETE"]
    )
    bp.add_url_rule("/shipping_methods", view_func=shipping_methods)
    bp.add_url_rule(
        "/shipping_methods/create",
        view_func=shipping_methods_manage,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/shipping_methods/<id>/edit",
        view_func=shipping_methods_manage,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/shipping_methods/<int:id>/delete",
        view_func=shipping_methods_del,
        methods=["DELETE"],
    )
    bp.add_url_rule("/products", view_func=products)
    bp.add_url_rule("/products/<id>", view_func=product_detail)
    bp.add_url_rule(
        "/products/create/step1",
        view_func=product_create_step1,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/products/create/step2",
        view_func=product_manage,
        methods=["GET", "POST"],
    )
    bp.add_url_rule(
        "/products/<id>/edit", view_func=product_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/products/<int:id>/delete", view_func=product_del, methods=["DELETE"]
    )
    bp.add_url_rule(
        "/products/variant/create", view_func=variant_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/products/variant/<id>/edit", view_func=variant_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/variants/<int:id>/delete", view_func=variant_del, methods=["DELETE"]
    )
    bp.add_url_rule("/orders", view_func=orders)
    bp.add_url_rule("/orders/<id>", view_func=order_detail)
    bp.add_url_rule("/orders/<id>/send", view_func=send_order)
    bp.add_url_rule("/orders/<id>/draft", view_func=draft_order)
    bp.add_url_rule("/vouchers", view_func=vouchers)
    bp.add_url_rule(
        "/vouchers/create", view_func=vouchers_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/vouchers/<id>/edit", view_func=vouchers_manage, methods=["GET", "POST"]
    )
    bp.add_url_rule(
        "/vouchers/<int:id>/delete", view_func=voucher_del, methods=["DELETE"]
    )
    bp.add_url_rule("/sales", view_func=sales)
    bp.add_url_rule("/sales/create", view_func=sales_manage, methods=["GET", "POST"])
    bp.add_url_rule("/sales/<id>/edit", view_func=sales_manage, methods=["GET", "POST"])
    bp.add_url_rule("/sales/<int:id>/delete", view_func=sale_del, methods=["DELETE"])

    app.register_blueprint(bp, url_prefix="/dashboard")
