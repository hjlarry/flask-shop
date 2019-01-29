from functools import wraps
from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import login_required, current_user

from flaskshop.account.models import User, UserAddress
from flaskshop.public.models import MenuItem

from .models import DashboardMenu
from .forms import DashboardMenuForm

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@blueprint.context_processor
def inject_param():
    menus = DashboardMenu.query.filter_by(parent_id=0).all()
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


@blueprint.route("/list")
def list():
    return render_template("dashboard/list.html")


@blueprint.route("/users")
def users():
    users = User.query.all()
    props = {
        "id": "ID",
        "username": "Username",
        "email": "Email",
        "active": "Is Active",
        "is_admin": "Is Admin",
    }
    return render_template("dashboard/list.html", props=props, items=users)


@blueprint.route("/menus")
def menus():
    menus = MenuItem.query.all()
    props = {
        "id": "ID",
        "title": "Title",
        "order": "Order",
        "site_id": "Site Id",
        "parent_id": "Parent Id",
    }
    return render_template("dashboard/list.html", props=props, items=menus)


@blueprint.route("/dashboard_menus")
def dashboard_menus():
    dashboard_menus = DashboardMenu.query.all()
    props = {
        "id": "ID",
        "title": "Title",
        "order": "Order",
        "endpoint": "Endpoint",
        "icon_cls": "Icon class",
        "parent_id": "Parent Id",
    }
    return render_template("dashboard/list.html", props=props, items=dashboard_menus)


@blueprint.route("/dashboard_menus/create", methods=["GET", "POST"])
def dashboard_menus_create():
    form = DashboardMenuForm()
    if form.validate_on_submit():
        menu = DashboardMenu()
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.dashboard_menus"))
    parents = DashboardMenu.first_level_items()
    return render_template("dashboard/dashboard_menu.html", form=form, parents=parents)


@blueprint.route("/dashboard_menus/<menu_id>/edit", methods=["GET", "POST"])
def dashboard_menus_edit(menu_id):
    menu = DashboardMenu.get_by_id(menu_id)
    form = DashboardMenuForm(obj=menu)
    if form.validate_on_submit():
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.dashboard_menus"))
    parents = DashboardMenu.first_level_items()
    return render_template("dashboard/dashboard_menu.html", form=form, parents=parents)
