# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy import or_

from .models import Product

blueprint = Blueprint(
    "product", __name__, url_prefix="/products", static_folder="../static"
)


@blueprint.route("/")
def index():
    """List products."""
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", None)
    build = Product.query.filter_by(on_sale=True)
    if search:
        build = build.filter(
            or_(
                Product.title.like("%" + search + "%"),
                Product.description.like("%" + search + "%"),
            )
        )
    pagination = build.paginate(page, per_page=16)
    products = pagination.items
    return render_template(
        "products/index.html", products=products, pagination=pagination
    )


@blueprint.route("/<id>")
def show(id):
    """show a product."""
    product = Product.query.filter_by(id=id).first()
    favored = False
    if not product.on_sale:
        flash("The product is not on sale", "warning")
        return redirect(url_for("product.index"))
    if current_user.is_authenticated:
        favored = product in current_user.favor_products

    return render_template("products/show.html", product=product, favored=favored)
