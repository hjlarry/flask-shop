import time
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    current_app,
    url_for,
    abort,
)
from flask_login import login_required, current_user

from .models import Order, OrderLine, OrderNote, OrderPayment
from .payment import zhifubao
from flaskshop.extensions import csrf_protect
from flaskshop.constant import ShipStatusKinds, PaymentStatusKinds, OrderStatusKinds

blueprint = Blueprint("order", __name__, url_prefix="/orders")


@blueprint.route("/")
@login_required
def index():
    return redirect(url_for("account.index"))


@blueprint.route("/<string:token>")
@login_required
def show(token):
    order = Order.query.filter_by(token=token).first()
    if not order.is_self_order:
        abort(403, "This is not your order!")
    return render_template("orders/details.html", order=order)


def create_payment(token, payment_method):
    order = Order.query.filter_by(token=token).first()
    if order.status != OrderStatusKinds.unfulfilled.value:
        abort(403, "This Order Can Not Pay")
    payment_no = str(int(time.time())) + str(current_user.id)
    customer_ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    payment = OrderPayment.query.filter_by(order_id=order.id).first()
    if payment:
        payment.update(
            payment_method=payment_method,
            payment_no=payment_no,
            customer_ip_address=customer_ip_address,
        )
    else:
        payment = OrderPayment.create(
            order_id=order.id,
            payment_method=payment_method,
            payment_no=payment_no,
            status=PaymentStatusKinds.waiting.value,
            total=order.total,
            customer_ip_address=customer_ip_address,
        )
    if payment_method == "alipay":
        order_string = zhifubao.send_order(order.token, payment_no, order.total)
        payment.order_string = order_string
    return payment


@blueprint.route("/pay/<string:token>/alipay")
@login_required
def ali_pay(token):
    payment = create_payment(token, "alipay")
    return redirect(current_app.config["PURCHASE_URI"] + payment.order_string)


@blueprint.route("/alipay/notify", methods=["POST"])
@csrf_protect.exempt
def ali_notify():
    data = request.form.to_dict()
    signature = data.pop("sign")
    success = zhifubao.verify_order(data, signature)
    if success:
        order_payment = OrderPayment.query.filter_by(
            payment_no=data["out_trade_no"]
        ).first()
        order_payment.pay_success(paid_at=data["gmt_payment"])
    return "", 200


# for test pay flow 
@blueprint.route("/pay/<string:token>/testpay")
@login_required
def test_pay(token):
    payment = create_payment(token, "testpay")
    payment.pay_success(paid_at=datetime.now())
    return redirect(url_for("order.payment_success"))


@blueprint.route("/payment_success")
@login_required
def payment_success():
    return render_template("orders/checkout_success.html")


@blueprint.route("/cancel/<string:token>")
@login_required
def cancel_order(token):
    order = Order.query.filter_by(token=token).first()
    if not order.is_self_order:
        abort(403, "This is not your order!")
    order.cancel()
    return render_template("orders/details.html", order=order)


@blueprint.route("/receive/<string:token>")
@login_required
def receive(token):
    order = Order.query.filter_by(token=token).first()
    order.update(
        status = OrderStatusKinds.completed.value,
        ship_status=ShipStatusKinds.received.value,
        )
    return render_template("orders/details.html", order=order)
