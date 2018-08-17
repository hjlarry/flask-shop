# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template, request

from flaskshop.extensions import login_manager
from flaskshop.account.models import User
from flaskshop.product.models import Product

blueprint = Blueprint("public", __name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/")
def home():
    products = Product.query.filter_by(is_featured=True).limit(8)
    return render_template("home.html", products=products)


@blueprint.route("/style")
def style():
    return render_template("style_guide.html")


@blueprint.route("/search")
def search():
    query = request.args.get('q', None)
    products = Product.query.whoosh_search(query).all()
    return render_template("search_result.html", products=products, query=query)
