from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from .models import UserCart

blueprint = Blueprint('cart', __name__, url_prefix='/cart', static_folder='../static')


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route('/')
def carts():
    """List cartItems."""
    cart_items = current_user.cart_items
    addresses = current_user.addresses
    return render_template('cart/index.html', cart_items=cart_items, addresses=addresses)


@blueprint.route('/add', methods=['POST'])
def cart_add():
    """Add items to cart"""
    data = request.get_json()
    UserCart.create(
        user=current_user,
        product_sku_id=data['sku_id'],
        amount=data['amount']
    )
    return Response(status=200)


@blueprint.route('/<id>', methods=['DELETE'])
def cart_del(id):
    """Delete an item of a user`s cart"""
    cart = UserCart.query.filter_by(id=id).first()
    if cart in current_user.cart_items:
        UserCart.delete(cart)
    return Response(status=200)
