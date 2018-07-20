from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response
from sqlalchemy import and_
import json

from .models import Cart, CouponCode

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
