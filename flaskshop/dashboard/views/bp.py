from functools import wraps
from flask import Blueprint, render_template, abort, redirect
from flask_login import login_required, current_user

from flaskshop.dashboard.models import DashboardMenu
from .user import users
from .site import site_menus, dashboard_menus, dashboard_menus_manage

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@blueprint.context_processor
def inject_param():
    menus = DashboardMenu.first_level_items()
    return {"menus": menus}


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(401)
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
    return render_template("dashboard/index.html")


blueprint.add_url_rule("/users", view_func=users)
blueprint.add_url_rule("/menus", view_func=site_menus)
blueprint.add_url_rule("/dashboard_menus", view_func=dashboard_menus)
blueprint.add_url_rule(
    "/dashboard_menus/create", view_func=dashboard_menus_manage, methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/dashboard_menus/<menu_id>/edit",
    view_func=dashboard_menus_manage,
    methods=["GET", "POST"],
)

