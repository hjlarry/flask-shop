from flask import render_template, redirect, url_for, request

from flaskshop.public.models import MenuItem, Page
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.product.models import Category, Collection
from flaskshop.dashboard.forms import DashboardMenuForm, SiteMenuForm


def site_menus():
    page = request.args.get("page", type=int, default=1)
    pagination = MenuItem.query.paginate(page, 10)
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
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("dashboard/list.html", **context)


def site_menus_manage(menu_id=None):
    if menu_id:
        menu = MenuItem.get_by_id(menu_id)
    else:
        menu = MenuItem()
    form = SiteMenuForm(obj=menu)
    if form.validate_on_submit():
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.site_menus"))
    parents = MenuItem.first_level_items()
    categories = Category.query.all()
    collections = Collection.query.all()
    pages = Page.query.all()
    context = {
        "form": form,
        "parents": parents,
        "categories": categories,
        "collections": collections,
        "pages": pages,
    }
    return render_template("dashboard/site_menu.html", **context)


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


def site_pages():
    pages = Page.query.all()
    props = {
        "id": "ID",
        "title": "Title",
        "slug": "Slug",
        "url": "Url",
        "is_visible": "Is Open",
    }
    context = {
        "title": "Site Pages",
        "manage_endpoint": "dashboard.dashboard_menus_manage",
        "items": pages,
        "props": props,
    }
    return render_template("dashboard/list.html", **context)
