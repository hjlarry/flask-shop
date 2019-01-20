# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user

from .forms import AddressForm, LoginForm, RegisterForm, ChangePasswordForm
from .models import UserAddress, User
from flaskshop.utils import flash_errors

blueprint = Blueprint("account", __name__, url_prefix="/account")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """login page."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        redirect_url = request.args.get("next") or url_for("public.home")
        flash("You are log in.", "success")
        return redirect(redirect_url)
    else:
        flash_errors(form)
    return render_template("account/login.html", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User.create(
            username=form.username.data,
            email=form.email.data.lower(),
            password=form.password.data,
            active=True,
        )
        login_user(user)
        flash("You are signed up.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("account/signup.html", form=form)


@blueprint.route("/")
def index():
    form = ChangePasswordForm(request.form)
    return render_template("account/details.html", form=form)


@blueprint.route("/setpwd", methods=["POST"])
def set_password():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        current_user.update(password=form.password.data)
        flash("You have changed password.", "success")
    else:
        flash_errors(form)
    return redirect(url_for("account.index"))


@blueprint.route("/address")
def addresses():
    """List addresses."""
    addresses = current_user.addresses
    return render_template("account/addresses.html", addresses=addresses)


@blueprint.route("/address/edit", methods=["GET", "POST"])
def edit_address():
    """Create and edit an address."""
    form = AddressForm(request.form)
    address_id = request.args.get("id", None, type=int)
    if address_id:
        user_address = UserAddress.get_by_id(address_id)
        form = AddressForm(request.form, obj=user_address)
    if request.method == "POST" and form.validate_on_submit():
        address_data = {
            "province": form.province.data,
            "city": form.city.data,
            "district": form.district.data,
            "address": form.address.data,
            "contact_name": form.contact_name.data,
            "contact_phone": form.contact_phone.data,
        }
        if address_id:
            UserAddress.update(user_address, **address_data)
            flash("Success edit address.", "success")
        else:
            UserAddress.create(**address_data)
            flash("Success add address.", "success")
        return redirect(url_for("account.index") + "#addresses")
    else:
        flash_errors(form)
    return render_template(
        "account/address_edit.html", form=form, address_id=address_id
    )


@blueprint.route("/address/<int:id>/delete", methods=["POST"])
def delete_address(id):
    user_address = UserAddress.get_by_id(id)
    if user_address in current_user.addresses:
        UserAddress.delete(user_address)
    return redirect(url_for("account.index") + "#addresses")
