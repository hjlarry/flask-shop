# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template, request, send_from_directory

from flaskshop.extensions import login_manager
from flaskshop.account.models import User
from flaskshop.product.models import Product
from .models import Page

blueprint = Blueprint("public", __name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/")
def home():
    products = Product.get_featured_product()
    return render_template("public/home.html", products=products)


@blueprint.route("/style")
def style():
    return render_template("public/style_guide.html")


@blueprint.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon-32x32.png")


@blueprint.route("/search")
def search():
    query = request.args.get("q", None)
    products = Product.query.whoosh_search(query).all()
    return render_template("public/search_result.html", products=products, query=query)


@blueprint.route("/page/<identity>")
def show_page(identity):
    page = Page.get_by_identity(identity)
    return render_template("public/page.html", page=page)
