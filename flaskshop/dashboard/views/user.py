from flask import render_template, redirect, url_for

from flaskshop.account.models import User, UserAddress
from flaskshop.order.models import Order
from flaskshop.dashboard.forms import UserForm, UserAddressForm


def users():
    users = User.query.all()
    props = {
        "id": "ID",
        "username": "Username",
        "email": "Email",
        "is_active": "Is Active",
        "is_admin": "Is Admin",
    }
    return render_template(
        "user/list.html", props=props, items=users, title="User List"
    )


def user(user_id):
    user = User.get_by_id(user_id)
    addresses = user.addresses
    orders = Order.get_user_orders(user_id)
    context = {"user": user, "addresses": addresses, "orders": orders}
    return render_template("user/detail.html", **context)


def user_edit(user_id):
    user = User.get_by_id(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        if not form.password.data:
            del form.password
        form.populate_obj(user)
        user.save()
        return redirect(url_for("dashboard.user", user_id=user_id))
    return render_template("user/edit.html", form=form)


def address_edit(id):
    addr = UserAddress.get_by_id(id)
    form = UserAddressForm(obj=addr)
    if form.validate_on_submit():
        form.populate_obj(addr)
        addr.save()
        return redirect(url_for("dashboard.user", user_id=addr.user_id))
    return render_template("user/edit_addr.html", form=form)
