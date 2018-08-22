# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template, request

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
    products = Product.query.filter_by(is_featured=True).limit(8)
    return render_template("public/home.html", products=products)


@blueprint.route("/style")
def style():
    return render_template("public/style_guide.html")


@blueprint.route("/search")
def search():
    query = request.args.get('q', None)
    products = Product.query.whoosh_search(query).all()
    return render_template("public/search_result.html", products=products, query=query)


@blueprint.route("/page/<id>")
def show_page(id):
    page = Page.get_by_id(id)
    return render_template("public/page.html", page=page)
