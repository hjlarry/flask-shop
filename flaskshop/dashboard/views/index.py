from datetime import datetime

from sqlalchemy import func
from flask import render_template

from flaskshop.account.models import User
from flaskshop.constant import OrderEvents, OrderStatusKinds
from flaskshop.extensions import db
from flaskshop.order.models import Order, OrderEvent, OrderLine
from flaskshop.product.models import Product


def index():
    def get_today_num(model):
        target = db.cast(datetime.now(), db.DATE)
        which = db.cast(model.created_at, db.DATE)
        return model.query.filter(which == target).count()

    def get_order_status(status):
        return {
            "count": Order.query.filter_by(status=status).count(),
            "kind": status,
        }

    onsale_products_count = Product.query.filter_by(on_sale=True).count()

    hot_product_ids = (
        db.session.query(OrderLine.product_id, func.count(OrderLine.product_id))
        .group_by(OrderLine.product_id)
        .order_by(func.count(OrderLine.product_id).desc())
        .all()
    )
    top5_products = []
    for product_id, order_count in hot_product_ids[:5]:
        p = Product.get_by_id(product_id)
        # product may deleted
        if not p:
            continue
        p.order_count = order_count
        top5_products.append(p)

    activity = OrderEvent.query.order_by(OrderEvent.id.desc()).limit(10)

    context = {
        "orders_total": Order.query.count(),
        "orders_today": get_today_num(Order),
        "users_total": User.query.count(),
        "users_today": get_today_num(User),
        "order_unfulfill": get_order_status(OrderStatusKinds.unfulfilled.value),
        "order_fulfill": get_order_status(OrderStatusKinds.fulfilled.value),
        "onsale_products_count": onsale_products_count,
        "top_products": top5_products,
        "activity": activity,
        "order_events": OrderEvents,
    }
    return render_template("index.html", **context)
