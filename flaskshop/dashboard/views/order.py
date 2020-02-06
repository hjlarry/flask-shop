from flask import request, render_template

from flaskshop.order.models import Order
from flaskshop.constant import OrderStatusKinds, ShipStatusKinds


def orders():
    page = request.args.get("page", type=int, default=1)
    pagination = Order.query.order_by(Order.id.desc()).paginate(page, 10)
    props = {
        "id": "ID",
        "identity": "Identity",
        "status_human": "Status",
        "total_human": "Total",
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


def send_order(id):
    order = Order.get_by_id(id)
    order.status = OrderStatusKinds.shipped.value
    order.ship_status = ShipStatusKinds.delivered.value
    order.save()
    return render_template("order/detail.html", order=order)


def draft_order(id):
    order = Order.get_by_id(id)
    order.status = OrderStatusKinds.draft.value
    order.save()
    return render_template("order/detail.html", order=order)
