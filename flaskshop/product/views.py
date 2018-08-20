# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template, request
from flask_login import login_required

from .models import Product, Category
from .forms import AddCartForm
from .utils import get_product_attributes_data, get_product_list_context, add_to_currentuser_cart

blueprint = Blueprint("product", __name__, url_prefix="/products")


@blueprint.route("/<id>")
def show(id, form=None):
    product = Product.get_by_id(id)
    if not form:
        form = AddCartForm(request.form, product=product)
    product_attributes = get_product_attributes_data(product)
    return render_template("products/details.html", product=product, form=form, product_attributes=product_attributes)


@blueprint.route("/<id>/add", methods=['POST'])
@login_required
def product_add_to_cart(id):
    """ this method return to the show method and use a form instance for display validater errors"""
    product = Product.get_by_id(id)
    form = AddCartForm(request.form, product=product)

    if form.validate_on_submit():
        add_to_currentuser_cart(form.quantity.data, form.variant.data)
    return show(id, form=form)


@blueprint.route("/category/<id>")
def show_category(id):
    page = request.args.get("page", 1, type=int)
    category = Category.get_by_id(id)
    items = category.products
    if category.children:
        for child in category.children:
            items.extend(child.products)
    ctx, items = get_product_list_context(request, items)
    pagination = items.paginate(page, per_page=16)
    products = pagination.items
    ctx.update(object=category, pagination=pagination, products=products)
    return render_template("category/index.html", **ctx)
