# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from werkzeug.wrappers import Response

from .models import Product
from .forms import AddCartForm
from .utils import get_product_attributes_data
from flaskshop.extensions import db

blueprint = Blueprint("product", __name__, url_prefix="/products")


@blueprint.route("/")
def index():
    """List products."""
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", None)
    order = request.args.get("order", None)
    build = Product.query.filter_by(on_sale=True)
    if search:
        build = build.filter(
            or_(
                Product.title.like("%" + search + "%"),
                Product.description.like("%" + search + "%"),
            )
        )
    if order:
        col, ord = order.split('-')
        if col in ('price', 'sold_count', 'rating') and ord in ('desc', 'asc'):
            col = getattr(Product, col)
            ord = getattr(col, ord)
            build = build.order_by(ord())
    pagination = build.paginate(page, per_page=16)
    products = pagination.items
    return render_template(
        "products/index.html", products=products, pagination=pagination
    )


@blueprint.route("/<id>")
def show(id):
    """show a product."""
    product = Product.query.filter_by(id=id).first()
    form = AddCartForm(product, request.form)
    product_attributes = get_product_attributes_data(product)
    favored = False  # TODO
    return render_template("products/details.html", product=product, form=form, product_attributes=product_attributes)


@blueprint.route("/<id>/favor", methods=['POST', 'DELETE'])
@login_required
def favor(id):
    """favor a product."""
    product = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        current_user.favor_products.append(product)
    else:
        current_user.favor_products.remove(product)
    db.session.commit()
    return Response(status=200)


@blueprint.route("/myfavor")
@login_required
def favorites():
    """a user`s favorite products"""
    page = request.args.get("page", 1, type=int)
    pagination = current_user.favor_products.paginate(page, per_page=16)
    products = pagination.items
    return render_template(
        "products/index.html", products=products, pagination=pagination
    )
