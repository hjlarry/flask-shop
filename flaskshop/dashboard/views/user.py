from flask import render_template

from flaskshop.account.models import User, UserAddress


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
        "dashboard/user_list.html", props=props, items=users, title="User List"
    )


def user(user_id):
    return render_template("dashboard/user_detail.html")
