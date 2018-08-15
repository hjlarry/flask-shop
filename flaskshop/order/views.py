from flask import Blueprint, render_template, request, redirect, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.wrappers import Response
from sqlalchemy import desc
import uuid
import json
import time

from .models import Order, OrderLine, OrderNote, OrderPayment
from .payment import zhifubao
from flaskshop.extensions import csrf_protect
from flaskshop.account.models import UserAddress
from flaskshop.checkout.models import Cart,CouponCode
from flaskshop.constant import REFUND_STATUS_APPLIED, SHIP_STATUS_RECEIVED

blueprint = Blueprint("order", __name__, url_prefix="/orders")


@blueprint.route("/")
@login_required
def index():
    """List orders."""
    page = request.args.get("page", 1, type=int)
    pagination = current_user.orders.order_by(desc(Order.created_at)).paginate(
        page, per_page=16
    )
    orders = pagination.items
    return render_template("orders/index.html", orders=orders, pagination=pagination)


@blueprint.route("/<id>")
@login_required
def show(id):
    """Show an order."""
    order = Order.query.filter_by(id=id).first()
    return render_template("orders/show.html", order=order)


# @blueprint.route("/", methods=["POST"])
# @login_required
# def store():
#     """From cart store an order."""
#     data = request.get_json()
#     address = UserAddress.query.filter_by(id=data["address_id"]).first()
#     total_amount = 0
#     items = []
#     coupon = None
#     if data["coupon_code"]:
#         coupon = CouponCode.query.filter_by(code=data["coupon_code"]).first()
#         try:
#             coupon.check_available(order_total_amount=total_amount)
#         except Exception as e:
#             return Response(e.args, status=422)
#     for item in data["items"]:
#         cart_item = Cart.query.filter_by(id=item["item_id"]).first()
#         amount = int(item["amount"])
#         try:
#             cart_item.product_sku.decrement_stock(amount)
#         except Exception as e:
#             return Response(e.args, status=422)
#         # order_item = OrderItem(
#         #     product_sku=cart_item.product_sku,
#         #     product=cart_item.product_sku.product,
#         #     amount=amount,
#         #     price=cart_item.product_sku.price,
#         # )
#         total_amount = total_amount + order_item.amount * order_item.price
#         cart_item.release(amount)
#         items.append(order_item)
#
#     if not items:
#         return Response("Need choose an item first", status=422)
#     if coupon:
#         total_amount = coupon.get_adjusted_price(order_total_amount=total_amount)
#         coupon.used += 1
#
#     order = Order.create(
#         user=current_user,
#         no=str(uuid.uuid1()),
#         address=address.full_address + address.contact_name + address.contact_phone,
#         remark=data["remark"],
#         total_amount=total_amount,
#         coupon_code=coupon,
#         items=items,
#     )
#     res = {"id": order.id}
#     return Response(json.dumps(res), status=200, mimetype="application/json")


@blueprint.route("/pay/<id>/alipay")
@login_required
def ali_pay(id):
    order = Order.query.filter_by(id=id).first()
    payment_no = str(int(time.time())) + str(current_user.id)
    order_string = zhifubao.send_order(order.no, payment_no, order.total_amount)
    order.update(payment_method="alipay", payment_no=payment_no)
    return redirect(current_app.config["PURCHASE_URI"] + order_string)


@blueprint.route("/alipay/notify", methods=["POST"])
@csrf_protect.exempt
def ali_notify():
    data = request.form.to_dict()
    signature = data.pop("sign")
    success = zhifubao.verify_order(data, signature)
    if success:
        order = Order.query.filter_by(payment_no=data["out_trade_no"]).first()
        order.update(paid_at=data["gmt_payment"])
    return Response(status=200)


@blueprint.route("/<id>/review", methods=["GET", "POST"])
@login_required
def review(id):
    """Review an order."""
    order = Order.query.filter_by(id=id).first()
    if request.method == "POST" and order.can_review():
        for item in order.items:
            item.update(
                review=request.form.get("review" + str(item.id)),
                rating=request.form.get("rating" + str(item.id)),
                reviewed_at=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            )
        order.update(reviewed=True)
        return redirect(url_for("order.index"))
    return render_template("orders/review.html", order=order)


@blueprint.route("/<id>/refund", methods=["POST"])
@login_required
def request_refund(id):
    order = Order.query.filter_by(id=id).first()
    try:
        order.can_refund()
    except Exception as e:
        return Response(e.args, status=422)
    reason = request.get_json()["reason"]
    extra = order.extra if order.extra else dict()
    extra["refund_reason"] = reason
    order.update(refund_status=REFUND_STATUS_APPLIED, extra=extra)
    return Response(status=200)


@blueprint.route("/<id>/received", methods=["POST"])
@login_required
def received(id):
    order = Order.query.filter_by(id=id).first()
    try:
        order.can_review()
    except Exception as e:
        return Response(e.args, status=422)
    order.update(ship_status=SHIP_STATUS_RECEIVED)
    return Response(status=200)
