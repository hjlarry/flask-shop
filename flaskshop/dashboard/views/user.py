from flask import render_template

from flaskshop.account.models import User, UserAddress
from flaskshop.order.models import Order


def users():
    users = User.query.all()
    props = {
        "id": "ID",
        "username": "Username",
        "email": "Email",
        "active": "Is Active",
        "is_admin": "Is Admin",
    }
    return render_template(
        "dashboard/user/user_list.html", props=props, items=users, title="User List"
    )


def user(user_id):
    user = User.get_by_id(user_id)
    addresses = user.addresses
    orders = Order.get_user_orders(user_id)
    context = {"user": user, "addresses": addresses, "orders": orders}
    return render_template("dashboard/user/user_detail.html", **context)
