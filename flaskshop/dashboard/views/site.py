from flask import render_template, redirect, url_for, request

from flaskshop.public.models import MenuItem, Page, Site
from flaskshop.dashboard.models import DashboardMenu
from flaskshop.product.models import Category, Collection
from flaskshop.account.utils import admin_required, permission_required, Permission
from flaskshop.dashboard.forms import DashboardMenuForm, SiteMenuForm, SitePageForm, SiteConfigForm


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
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "site_menus",
    }
    return render_template("list.html", **context)


@admin_required
def site_menus_manage(id=None):
    if id:
        menu = MenuItem.get_by_id(id)
        form = SiteMenuForm(obj=menu)
    else:
        form = SiteMenuForm()

    if form.validate_on_submit():
        if not id:
            menu = MenuItem()
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
    return render_template("site/site_menu.html", **context)


def dashboard_menus():
    page = request.args.get("page", type=int, default=1)
    pagination = DashboardMenu.query.paginate(page, 10)
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
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "dashboard_menus",
    }
    return render_template("list.html", **context)


@admin_required
def dashboard_menus_manage(id=None):
    if id:
        menu = DashboardMenu.get_by_id(id)
        form = DashboardMenuForm(obj=menu)
    else:
        form = DashboardMenuForm()
    if form.validate_on_submit():
        if not id:
            menu = DashboardMenu()
        form.populate_obj(menu)
        menu.save()
        return redirect(url_for("dashboard.dashboard_menus"))
    parents = DashboardMenu.first_level_items()
    return render_template("site/dashboard_menu.html", form=form, parents=parents)


def site_pages():
    page = request.args.get("page", type=int, default=1)
    pagination = Page.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "slug": "Slug",
        "url": "Url",
        "is_visible": "Is Visiable",
    }
    context = {
        "title": "Site Pages",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "site_pages",
    }
    return render_template("list.html", **context)


def site_pages_manage(id=None):
    if id:
        page = Page.get_by_id(id)
        form = SitePageForm(obj=page)
    else:
        form = SitePageForm()
    if form.validate_on_submit():
        if not id:
            page = Page()
        form.populate_obj(page)
        page.save()
        return redirect(url_for("dashboard.site_pages"))
    return render_template("site/site_page.html", form=form)


def site_config():
    site = Site.query.first()
    form = SiteConfigForm(obj=site)
    if form.validate_on_submit():
        form.populate_obj(site)
        site.save()
        return redirect(url_for("dashboard.site_config"))
    return render_template("site/site_config.html", form=form)
