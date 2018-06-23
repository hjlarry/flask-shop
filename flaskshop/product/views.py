# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, render_template

from .models import Product

blueprint = Blueprint(
    "product", __name__, url_prefix="/products", static_folder="../static"
)


@blueprint.route("/")
def index():
    """List products."""
    products = Product.query.all()
    return render_template("products/index.html", products=products)


@blueprint.route("/<id>")
def show(id):
    """show a product."""
    product = Product.query.filter_by(id=id).first()
    return render_template("products/show.html", product=product)

