from flask import render_template, redirect, url_for, request, flash

from flaskshop.public.models import MenuItem, Page
from flaskshop.dashboard.models import DashboardMenu, Setting
from flaskshop.product.models import Category, Collection
from flaskshop.checkout.models import ShippingMethod
from flaskshop.plugin.models import PluginRegistry
from flaskshop.account.utils import admin_required, permission_required, Permission
from flaskshop.dashboard.forms import (
    DashboardMenuForm,
    SiteMenuForm,
    SitePageForm,
    ShippingMethodForm,
    generate_settings_form,
)


def shipping_methods():
    page = request.args.get("page", type=int, default=1)
    pagination = ShippingMethod.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "price_human": "Price",
        "created_at": "Created At",
    }
    context = {
        "title": "Shipping Method",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "shipping_methods",
    }
    return render_template("list.html", **context)


def shipping_methods_manage(id=None):
    if id:
        shipping_method = ShippingMethod.get_by_id(id)
        form = ShippingMethodForm(obj=shipping_method)
    else:
        form = ShippingMethodForm()
    if form.validate_on_submit():
        if not id:
            shipping_method = ShippingMethod()
        form.populate_obj(shipping_method)
        shipping_method.save()
        return redirect(url_for("dashboard.shipping_methods"))
    return render_template("site/shipping_method.html", form=form)


def site_menus():
    page = request.args.get("page", type=int, default=1)
    pagination = MenuItem.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "order": "Order",
        "position": "Position",
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


def plugin_list():
    plugins = PluginRegistry.query.all()
    return render_template("site/plugin.html", plugins=plugins)


def plugin_enable(id):
    plugin = PluginRegistry.get_by_id(id)
    plugin.enabled = True
    plugin.save()
    flash("The plugin is enabled, Please restart flask-shop now!", "success")
    return redirect(url_for("dashboard.plugin_list"))


def plugin_disable(id):
    plugin = PluginRegistry.get_by_id(id)
    plugin.enabled = False
    plugin.save()
    flash("The plugin is disabled, Please restart flask-shop now!", "info")
    return redirect(url_for("dashboard.plugin_list"))


def site_setting():
    settings = Setting.query.all()
    form = generate_settings_form(settings)()

    old_settings = Setting.get_settings()
    if request.method == "GET":
        for key, value in old_settings.items():
            try:
                form[key].data = value
            except (KeyError, ValueError):
                pass

    if form.validate_on_submit():
        new_settings = {}
        for key, value in old_settings.items():
            try:
                # check if the value has changed
                if value == form[key].data:
                    continue
                else:
                    new_settings[key] = form[key].data
            except KeyError:
                pass
        Setting.update(settings=new_settings)
        flash("Settings saved.", "success")
    return render_template("site/settings.html", form=form,)


def config_index():
    return render_template("site/index.html")
