from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response
import json

from .models import Cart, CouponCode
from flaskshop.account.forms import AddressForm
from flaskshop.account.models import UserAddress

blueprint = Blueprint('checkout', __name__, url_prefix='/checkout')


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route('/cart')
def cart_index():
    if current_user.is_authenticated and current_user.cart:
        cart_lines = current_user.cart.lines
    else:
        cart_lines = None
    return render_template('checkout/index.html', cart_lines=cart_lines, shipping_required=None)


@blueprint.route('/coupon/<code>', methods=['POST'])
def verify(code):
    """check a coupon code"""
    coupon = CouponCode.query.filter_by(code=code).first()
    if not coupon:
        return Response('It`s not a correct code!', status=422)
    try:
        coupon.check_available()
    except Exception as e:
        return Response(e.args, status=422)
    res = {
        'description': coupon.description,
    }
    return Response(json.dumps(res), status=200)


@blueprint.route('/shipping_address', methods=['GET', 'POST'])
def checkout_shipping_address():
    form = AddressForm(request.form)
    if request.method == 'GET':
        return render_template('checkout/shipping_address.html', form=form)
    if request.form['address_sel'] == 'new':
        if not form.validate_on_submit():
            return
        user_address = UserAddress.create(
            province=form.province.data,
            city=form.city.data,
            district=form.district.data,
            address=form.address.data,
            contact_name=form.contact_name.data,
            contact_phone=form.contact_phone.data,
            user=current_user
        )
    else:
        user_address = UserAddress.get_by_id(request.form['address_sel'])
    current_user.cart.update(address=user_address)
    return redirect(url_for('checkout.checkout_shipping_method'))


@blueprint.route('/shipping_method')
def checkout_shipping_method():
    return render_template('checkout/shipping_method.html')
