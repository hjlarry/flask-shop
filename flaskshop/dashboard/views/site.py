from flask import render_template

from flaskshop.public.models import MenuItem
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.dashboard.forms import DashboardMenuForm


def menus():
    menus = MenuItem.query.all()
    props = {
        "id": "ID",
        "title": "Title",
        "order": "Order",
        "site_id": "Site Id",
        "parent_id": "Parent Id",
    }
    context = {
        "title": "Site Menus",
        "create_endpoint": "dashboard.dashboard_menus_create",
        "edit_endpoint": "dashboard.dashboard_menus_edit",
        "items": menus,
        "props": props,
    }
    return render_template("dashboard/list.html", **context)


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
    context = {
        "title": "Dashboard Menus",
        "create_endpoint": "dashboard.dashboard_menus_create",
        "edit_endpoint": "dashboard.dashboard_menus_edit",
        "items": dashboard_menus,
        "props": props,
    }
    return render_template("dashboard/list.html", **context)


def dashboard_menus_create():
    form = DashboardMenuForm()
    if form.validate_on_submit():
        menu = DashboardMenu()
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.dashboard_menus"))
    parents = DashboardMenu.first_level_items()
    return render_template("dashboard/dashboard_menu.html", form=form, parents=parents)


def dashboard_menus_edit(menu_id):
    menu = DashboardMenu.get_by_id(menu_id)
    form = DashboardMenuForm(obj=menu)
    if form.validate_on_submit():
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.dashboard_menus"))
    parents = DashboardMenu.first_level_items()
    return render_template("dashboard/dashboard_menu.html", form=form, parents=parents)
