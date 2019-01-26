from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required

from .models import CartLine, Cart
from .forms import ShippingMethodForm
from flaskshop.account.forms import AddressForm
from flaskshop.account.models import UserAddress
from flaskshop.order.models import Order, OrderLine, OrderNote
from flaskshop.constant import ORDER_STATUS_UNFULFILLED

blueprint = Blueprint("checkout", __name__, url_prefix="/checkout")


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route("/cart")
def cart_index():
    return render_template("checkout/cart.html")


@blueprint.route("/update_cart/<int:id>", methods=["POST"])
def update_cartline(id):
    line = CartLine.get_by_id(id)
    response = {
        "variantId": line.variant_id,
        "subtotal": 0,
        "total": 0,
        "cart": {"numItems": 0, "numLines": 0},
    }
    if request.form["quantity"] == "0":
        line.delete()
    else:
        line.quantity = int(request.form["quantity"])
        line.save()
    cart = Cart.query.filter(Cart.user_id == current_user.id).first()
    response["cart"]["numItems"] = cart.update_quantity()
    response["cart"]["numLines"] = len(cart)
    response["subtotal"] = "$" + str(line.subtotal)
    response["total"] = "$" + str(cart.total)
    return jsonify(response)


# @blueprint.route('/coupon/<code>', methods=['POST'])
# def verify(code):
#     """check a coupon code"""
#     coupon = CouponCode.query.filter_by(code=code).first()
#     if not coupon:
#         return Response('It`s not a correct code!', status=422)
#     try:
#         coupon.check_available()
#     except Exception as e:
#         return Response(e.args, status=422)
#     res = {
#         'description': coupon.description,
#     }
#     return Response(json.dumps(res), status=200)


@blueprint.route("/shipping_address", methods=["GET", "POST"])
def checkout_shipping_address():
    form = AddressForm(request.form)
    if request.method == "GET":
        return render_template("checkout/shipping_address.html", form=form)
    if request.form["address_sel"] == "new":
        if not form.validate_on_submit():
            return
        user_address = UserAddress.create(
            province=form.province.data,
            city=form.city.data,
            district=form.district.data,
            address=form.address.data,
            contact_name=form.contact_name.data,
            contact_phone=form.contact_phone.data,
            user=current_user,
        )
    else:
        user_address = UserAddress.get_by_id(request.form["address_sel"])
    cart = Cart.get_current_user_cart()
    cart.update(shipping_address_id=user_address.id)
    return redirect(url_for("checkout.checkout_shipping_method"))


@blueprint.route("/shipping_method", methods=["GET", "POST"])
def checkout_shipping_method():
    form = ShippingMethodForm(request.form)
    if form.validate_on_submit():
        cart = Cart.get_current_user_cart()
        order = Order.create(
            user=current_user,
            shipping_method_id=form.shipping_method.data,
            shipping_address=cart.address,
            status=ORDER_STATUS_UNFULFILLED,
        )
        if form.note.data:
            OrderNote.create(order=order, user=current_user, content=form.note.data)
        total = 0
        for line in cart.lines:
            order_line = OrderLine.create(
                order=order,
                variant=line.variant,
                quantity=line.quantity,
                product_name=line.product.title,
                product_sku=line.variant.sku,
                unit_price_net=line.variant.price,
                is_shipping_required=line.variant.is_shipping_required,
            )
            total += order_line.get_total()
            line.delete()
        total += order.shipping_method.price
        order.update(
            total_net=total,
            shipping_method_name=order.shipping_method.title,
            shipping_price_net=order.shipping_method.price,
        )
        cart.delete()
        return redirect(order.get_absolute_url())
    return render_template("checkout/shipping_method.html", form=form)
