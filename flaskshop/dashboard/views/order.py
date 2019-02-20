from flask import request, render_template

from flaskshop.order.models import Order


def orders():
    page = request.args.get("page", type=int, default=1)
    pagination = Order.query.paginate(page, 10)
    props = {
        "id": "ID",
        "identity": "Identity",
        "status": "Status",
        "total_net": "Total",
        "user": "User",
        "created_at": "Created At",
    }
    context = {
        "title": "Order List",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("order/list.html", **context)


def order_detail(id):
    order = Order.get_by_id(id)
    return render_template("order/detail.html", order=order)
