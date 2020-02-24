# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from pluggy import HookimplMarker

from flaskshop.checkout.models import Cart

from .models import Product, Category, ProductCollection, ProductVariant
from .forms import AddCartForm


impl = HookimplMarker("flaskshop")


def show(id, form=None):
    product = Product.get_by_id(id)
    if not form:
        form = AddCartForm(request.form, product=product)
    return render_template("products/details.html", product=product, form=form)


@login_required
def product_add_to_cart(id):
    """ this method return to the show method and use a form instance for display validater errors"""
    product = Product.get_by_id(id)
    form = AddCartForm(request.form, product=product)

    if form.validate_on_submit():
        Cart.add_to_currentuser_cart(form.quantity.data, form.variant.data)
    return show(id, form=form)


def variant_price(id):
    variant = ProductVariant.get_by_id(id)
    return jsonify({"price": float(variant.price), "stock": variant.stock})


def show_category(id):
    page = request.args.get("page", 1, type=int)
    ctx = Category.get_product_by_category(id, page)
    return render_template("category/index.html", **ctx)


def show_collection(id):
    page = request.args.get("page", 1, type=int)
    ctx = ProductCollection.get_product_by_collection(id, page)
    return render_template("category/index.html", **ctx)


@impl
def flaskshop_load_blueprints(app):
    bp = Blueprint("product", __name__)
    bp.add_url_rule("/<int:id>", view_func=show)
    bp.add_url_rule("/api/variant_price/<int:id>", view_func=variant_price)
    bp.add_url_rule("/<int:id>/add", view_func=product_add_to_cart, methods=["POST"])
    bp.add_url_rule("/category/<int:id>", view_func=show_category)
    bp.add_url_rule("/collection/<int:id>", view_func=show_collection)

    app.register_blueprint(bp, url_prefix="/products")
