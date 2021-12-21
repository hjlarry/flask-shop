from flask import render_template, redirect, url_for, request
from sqlalchemy import or_
from flask_babel import lazy_gettext
from flaskshop.dashboard.models import Mail_Templates
# mail = current_app.extensions.get("mail")

def mails():
    page = request.args.get("page", type=int, default=1)
    pagination = Mail_Templates.query.paginate(page, 10)
    props = {
        "id": lazy_gettext("ID"),
        "title": lazy_gettext("Title"),
        "price_human": lazy_gettext("Price"),
        "created_at": lazy_gettext("Created At"),
    }
    context = {
        "title": lazy_gettext("Shipping Method"),
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "identity": "shipping_methods",
    }
    return render_template("list.html", **context)