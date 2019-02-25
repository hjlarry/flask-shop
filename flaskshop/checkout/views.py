from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required

from .models import CartLine, Cart, ShippingMethod
from .forms import NoteForm, VoucherForm
from flaskshop.account.forms import AddressForm
from flaskshop.account.models import UserAddress
from flaskshop.account.utils import flash_errors
from flaskshop.order.models import Order, OrderLine, OrderNote
from flaskshop.discount.models import Voucher
from flaskshop.constant import OrderStatusKinds

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
    # TODO when not enough stock, response ajax error
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


@blueprint.route("/shipping", methods=["GET", "POST"])
def checkout_shipping():
    form = AddressForm(request.form)
    user_address = None
    if request.method == "POST":
        if request.form["address_sel"] != "new":
            user_address = UserAddress.get_by_id(request.form["address_sel"])
        elif request.form["address_sel"] == "new" and form.validate_on_submit():
            user_address = UserAddress.create(
                province=form.province.data,
                city=form.city.data,
                district=form.district.data,
                address=form.address.data,
                contact_name=form.contact_name.data,
                contact_phone=form.contact_phone.data,
                user_id=current_user.id,
            )
        shipping_method = ShippingMethod.get_by_id(request.form["shipping_method"])
        if user_address and shipping_method:
            cart = Cart.get_current_user_cart()
            cart.update(
                shipping_address_id=user_address.id,
                shipping_method_id=shipping_method.id,
            )
            return redirect(url_for("checkout.checkout_note"))
    flash_errors(form)
    shipping_methods = ShippingMethod.query.all()
    return render_template(
        "checkout/shipping.html", form=form, shipping_methods=shipping_methods
    )


@blueprint.route("/note", methods=["GET", "POST"])
def checkout_note():
    form = NoteForm(request.form)
    voucher_form = VoucherForm(request.form)
    cart = Cart.get_current_user_cart()
    address = UserAddress.get_by_id(cart.shipping_address_id)
    shipping_method = ShippingMethod.get_by_id(cart.shipping_method_id)
    if form.validate_on_submit():
        order, msg = Order.create_whole_order(cart, form.note.data)
        if order:
            return redirect(order.get_absolute_url())
        else:
            flash(msg, "warning")
            return redirect(url_for("checkout.cart_index"))
    return render_template(
        "checkout/note.html",
        form=form,
        address=address,
        voucher_form=voucher_form,
        shipping_method=shipping_method,
    )


@blueprint.route("/voucher", methods=["POST"])
def checkout_voucher():
    voucher_form = VoucherForm(request.form)
    if voucher_form.validate_on_submit():
        voucher = Voucher.get_by_code(form.code.data)
        err_msg = None
        if voucher:
            try:
                voucher.check_available()
            except expression as e:
                err_msg = e
        else:
            err_msg = "Your code is not correct"
        if err_msg:
            flash(err_msg, "warning")
        else:
            cart = Cart.get_current_user_cart()
            cart.voucher_code = voucher.code
            cart.save()
        return redirect(url_for("checkout.checkout_note"))


@blueprint.route("/voucher/remove", methods=["POST"])
def checkout_voucher_remove():
    voucher_form = VoucherForm(request.form)
    if voucher_form.validate_on_submit():
        cart = Cart.get_current_user_cart()
        cart.voucher_code = None
        cart.save()
        return redirect(url_for("checkout.checkout_note"))
