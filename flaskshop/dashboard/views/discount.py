from flask import request, render_template

from flaskshop.discount.models import Voucher, Sale, SaleCategory, SaleProduct


def vouchers():
    page = request.args.get("page", type=int, default=1)
    pagination = Voucher.query.paginate(page, 10)
    props = {
        "id": "ID",
        "title": "Title",
        "type_label": "Type",
        "usage_limit": "Usage Limit",
        "used": "Used",
        "discount_value_type_label": "Discount Type",
        "discount_value": "Discount Value",
    }
    context = {
        "title": "Voucher",
        "manage_endpoint": "dashboard.attribute_manage",
        "items": pagination.items,
        "props": props,
        "pagination": pagination,
    }
    return render_template("list.html", **context)
