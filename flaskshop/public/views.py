# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from flaskshop.extensions import login_manager
from flaskshop.user.forms import RegisterForm, LoginForm
from flaskshop.user.models import User
from flaskshop.product.models import Product
from flaskshop.utils import flash_errors

blueprint = Blueprint("public", __name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/")
def home():
    """Home page."""
    products = Product.query.paginate(1, per_page=8).items
    return render_template("home.html", products=products)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """login page."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        flash("You are logged in.", "success")
        redirect_url = request.args.get("next") or url_for("user.members")
        return redirect(redirect_url)
    else:
        flash_errors(form)
    return render_template("public/login.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)
