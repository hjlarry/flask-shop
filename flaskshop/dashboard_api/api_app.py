import os
from functools import wraps

from flask import request, abort
from flask_login import current_user, login_required

from flaskshop.extensions import db, login_manager
from flaskshop.account.utils import admin_required
from flaskshop import settings
from .utils import ApiFlask, ApiResult
from .exceptions import ApiException, httperrors
from .views import (
    user_del,
    product_type_del,
    category_del,
    collection_del,
    attribute_del,
    variant_del,
    product_del,
    sale_del,
    dashboard_menu_del,
)


def create_app(config):
    app = ApiFlask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)
    return app


config = getattr(settings, os.environ.get("CURRENT_CONFIG"), "ProdConfig")
dashboard_api = create_app(config)


@dashboard_api.errorhandler(ApiException)
def api_error_handler(error):
    return error.to_result()


@dashboard_api.errorhandler(401)
@dashboard_api.errorhandler(403)
@dashboard_api.errorhandler(404)
@dashboard_api.errorhandler(500)
def error_handler(error):
    if hasattr(error, "name"):
        status = error.code
        if status == 403:
            msg = "无权限"
        else:
            msg = error.name
    else:
        msg = error.msg
        status = 500
    return ApiResult({"msg": msg, "r": 1, "status": status})


@dashboard_api.before_request
@admin_required
def before_request():
    pass


dashboard_api.add_url_rule(
    "/users/<int:id>/delete", view_func=user_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/product_type/<int:id>/delete", view_func=product_type_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/category/<int:id>/delete", view_func=category_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/collection/<int:id>/delete", view_func=collection_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/attribute/<int:id>/delete", view_func=attribute_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/variant/<int:id>/delete", view_func=variant_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/product/<int:id>/delete", view_func=product_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/sale/<int:id>/delete", view_func=sale_del, methods=["DELETE"]
)
dashboard_api.add_url_rule(
    "/dashboard_menus/<int:id>/delete", view_func=dashboard_menu_del, methods=["DELETE"]
)
