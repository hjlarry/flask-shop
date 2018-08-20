# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from .models import Product, Category
from .forms import AddCartForm
from .utils import get_product_attributes_data, get_product_list_context, add_to_currentuser_cart
from flaskshop.extensions import db

blueprint = Blueprint("product", __name__, url_prefix="/products")


@blueprint.route("/<id>")
def show(id, form=None):
    """show a product."""
    product = Product.get_by_id(id)
    if not form:
        form = AddCartForm(request.form, product=product)
    product_attributes = get_product_attributes_data(product)
    return render_template("products/details.html", product=product, form=form, product_attributes=product_attributes)


@blueprint.route("/<id>/add", methods=['POST'])
@login_required
def product_add_to_cart(id):
    """ Method return use same form instance for display validater errors"""
    product = Product.get_by_id(id)
    form = AddCartForm(request.form, product=product)

    if form.validate_on_submit():
        add_to_currentuser_cart(form.quantity.data, form.variant.data)
    return show(id, form=form)


@blueprint.route("/category/<id>")
def show_category(id):
    # TODO: filter query
    page = request.args.get("page", 1, type=int)
    category = Category.get_by_id(id)
    pagination = category.products.paginate(page, per_page=16)
    products = pagination.items
    ctx = get_product_list_context(request, products)
    ctx.update(object=category, pagination=pagination, products=products)
    return render_template("category/index.html", **ctx)


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
