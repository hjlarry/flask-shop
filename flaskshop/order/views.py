from flask import Blueprint, render_template, request, redirect, current_app, url_for, abort
from flask_login import login_required, current_user
import time

from .models import Order, OrderLine, OrderNote, OrderPayment
from .payment import zhifubao
from flaskshop.extensions import csrf_protect
from flaskshop.constant import REFUND_STATUS_APPLIED, SHIP_STATUS_RECEIVED, PAYMENT_STATUS_WAITING, \
    PAYMENT_STATUS_CONFIRMED

blueprint = Blueprint("order", __name__, url_prefix="/orders")


@blueprint.route("/")
@login_required
def index():
    """List orders."""
    return redirect(url_for('account.index'))


@blueprint.route("/<string:token>")
@login_required
def show(token):
    """Show an order."""
    order = Order.query.filter_by(token=token).first()
    if not order.is_self_order:
        return abort(403)
    return render_template("orders/details.html", order=order)


@blueprint.route("/pay/<string:token>/alipay")
@login_required
def ali_pay(token):
    order = Order.query.filter_by(token=token).first()
    payment_no = str(int(time.time())) + str(current_user.id)
    order_string = zhifubao.send_order(order.token, payment_no, order.total_net)
    customer_ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    OrderPayment.create(order=order, payment_method="alipay", payment_no=payment_no, status=PAYMENT_STATUS_WAITING,
                        total=order.total_net, customer_ip_address=customer_ip_address)
    return redirect(current_app.config["PURCHASE_URI"] + order_string)


@blueprint.route("/alipay/notify", methods=["POST"])
@csrf_protect.exempt
def ali_notify():
    data = request.form.to_dict()
    signature = data.pop("sign")
    success = zhifubao.verify_order(data, signature)
    if success:
        order_payment = OrderPayment.query.filter_by(payment_no=data["out_trade_no"]).first()
        order_payment.update(paid_at=data["gmt_payment"], status=PAYMENT_STATUS_CONFIRMED)
    return '', 200


@blueprint.route("/payment_success")
@login_required
def payment_success():
    return render_template("orders/checkout_success.html")


@blueprint.route("/<int:id>/refund", methods=["POST"])
@login_required
def request_refund(id):
    order = Order.get_by_id(id)
    try:
        order.can_refund()
    except Exception as e:
        return e.args, 422
    reason = request.get_json()["reason"]
    extra = order.extra if order.extra else dict()
    extra["refund_reason"] = reason
    order.update(refund_status=REFUND_STATUS_APPLIED, extra=extra)
    return '', 200


@blueprint.route("/<int:id>/received", methods=["POST"])
@login_required
def received(id):
    order = Order.get_by_id(id)
    try:
        order.can_review()
    except Exception as e:
        return e.args, 422
    order.update(ship_status=SHIP_STATUS_RECEIVED)
    return '', 200
