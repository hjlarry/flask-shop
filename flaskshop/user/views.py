# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from .forms import AddressForm
from .models import UserAddress
from flaskshop.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route("/")
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/address")
def addresses():
    """List addresses."""
    addresses = current_user.addresses
    return render_template("users/addresses.html", addresses=addresses)


@blueprint.route("/address/edit", methods=["GET", "POST"])
def edit_address():
    """Create and edit an address."""
    form = AddressForm(request.form)
    edit = request.args.get('id', None)
    user_address = UserAddress.query.filter_by(id=edit).first() if edit else None
    province_city = user_address.province +'/'+ user_address.city +'/'+user_address.district if user_address else None
    if form.validate_on_submit():
        province, city, district = form.province_city.data.split('/')
        if edit:
            UserAddress.update(
                user_address,
                province=province,
                city=city,
                district=district,
                address=form.address.data,
                contact_name=form.contact_name.data,
                contact_phone=form.contact_phone.data,
            )
            flash("Success edit address.", "success")
        else:
            UserAddress.create(
                province=province,
                city=city,
                district=district,
                address=form.address.data,
                contact_name=form.contact_name.data,
                contact_phone=form.contact_phone.data,
                user=current_user
            )
            flash("Success add address.", "success")
        return redirect(url_for("user.addresses"))
    else:
        flash_errors(form)
    return render_template("users/address_edit.html", form=form, user_address=user_address, province_city=province_city)


@blueprint.route("/address/<id>", methods=["DELETE"])
def delete_address(id):
    user_address = UserAddress.query.filter_by(id=id).first()
    if user_address in current_user.addresses:
        UserAddress.delete(user_address)
    return ''
