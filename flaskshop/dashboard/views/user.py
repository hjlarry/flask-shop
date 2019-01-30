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
    context = {}
    return render_template("dashboard/list.html", props=props, items=users)
