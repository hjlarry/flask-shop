from flask import render_template, redirect, url_for

from flaskshop.public.models import MenuItem
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.dashboard.forms import DashboardMenuForm, SiteMenuForm


def site_menus():
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
        "manage_endpoint": "dashboard.site_menus_manage",
        "items": menus,
        "props": props,
    }
    return render_template("dashboard/list.html", **context)


def site_menus_manage(menu_id=None):
    if menu_id:
        menu = MenuItem.get_by_id(menu_id)
    else:
        menu = MenuItem()
    form = SiteMenuForm(obj=menu)
    if form.validate_on_submit():
        if not form.category_id.data:
            del form.category_id
        if not form.collection_id.data:
            del form.collection_id
        if not form.page_id.data:
            del form.page_id
        if not form.parent_id.data:
            del form.parent_id
        else:
            del form.site_id
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.site_menus"))
    parents = MenuItem.first_level_items()
    return render_template("dashboard/site_menu.html", form=form, parents=parents)


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
        "manage_endpoint": "dashboard.dashboard_menus_manage",
        "items": dashboard_menus,
        "props": props,
    }
    return render_template("dashboard/list.html", **context)


def dashboard_menus_manage(menu_id=None):
    if menu_id:
        menu = DashboardMenu.get_by_id(menu_id)
    else:
        menu = DashboardMenu()
    form = DashboardMenuForm(obj=menu)
    if form.validate_on_submit():
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.dashboard_menus"))
    parents = DashboardMenu.first_level_items()
    return render_template("dashboard/dashboard_menu.html", form=form, parents=parents)
