from datetime import datetime

from flask import request, render_template

from flaskshop.order.models import Order
from flaskshop.constant import OrderStatusKinds


def orders():
    page = request.args.get("page", type=int, default=1)
    query = Order.query.order_by(Order.id.desc())

    status = request.args.get("status", type=int)
    if status:
        query = query.filter_by(status=status)
    order_no = request.args.get("order_number", type=str)
    if order_no:
        query = query.filter(Order.token.like(f"%{order_no}%"))
    created_at = request.args.get("created_at", type=str)
    if created_at:
        start_date, end_date = created_at.split("-")
        start_date = datetime.strptime(start_date.strip(), "%m/%d/%Y")
        end_date = datetime.strptime(end_date.strip(), "%m/%d/%Y")
        query = query.filter(Order.created_at.between(start_date, end_date))
    pagination = query.paginate(page, 10)
    props = {
        "id": "ID",
        "identity": "Identity",
        "status_human": "Status",
        "total_human": "Total",
        "user": "User",
        "created_at": "Created At",
    }
    context = {
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
        "order_stats_kinds": OrderStatusKinds,
    }
    return render_template("order/list.html", **context)


def order_detail(id):
    order = Order.get_by_id(id)
    return render_template("order/detail.html", order=order)


def send_order(id):
    order = Order.get_by_id(id)
    order.delivered()
    return render_template("order/detail.html", order=order)


def draft_order(id):
    order = Order.get_by_id(id)
    order.draft()
    return render_template("order/detail.html", order=order)
