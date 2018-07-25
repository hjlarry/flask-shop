# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template

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
    """Home page."""
    products = Product.query.filter_by(is_featured=True).limit(8)
    return render_template("home.html", products=products)
