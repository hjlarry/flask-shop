# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template, request
from flask_login import login_required

from .models import Product, Category, ProductCollection
from .forms import AddCartForm
from .utils import add_to_currentuser_cart

blueprint = Blueprint("product", __name__, url_prefix="/products")


@blueprint.route("/<int:id>")
def show(id, form=None):
    product = Product.get_by_id(id)
    if not form:
        form = AddCartForm(request.form, product=product)
    return render_template("products/details.html", product=product, form=form)


@blueprint.route("/<int:id>/add", methods=["POST"])
@login_required
def product_add_to_cart(id):
    """ this method return to the show method and use a form instance for display validater errors"""
    product = Product.get_by_id(id)
    form = AddCartForm(request.form, product=product)

    if form.validate_on_submit():
        add_to_currentuser_cart(form.quantity.data, form.variant.data)
    return show(id, form=form)


@blueprint.route("/category/<int:id>")
def show_category(id):
    page = request.args.get("page", 1, type=int)
    ctx = Category.get_product_by_category(id, page)
    return render_template("category/index.html", **ctx)


@blueprint.route("/collection/<int:id>")
def show_collection(id):
    page = request.args.get("page", 1, type=int)
    ctx = ProductCollection.get_product_by_collection(id, page)
    return render_template("category/index.html", **ctx)
