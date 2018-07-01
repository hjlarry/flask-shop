from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from werkzeug.wrappers import Response
from sqlalchemy import and_

from .models import UserCart
from flaskshop.product.models import ProductSku

blueprint = Blueprint('cart', __name__, url_prefix='/cart', static_folder='../static')


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route('/')
def index():
    """List cartItems."""
    cart_items = current_user.cart_items
    addresses = current_user.addresses
    return render_template('cart/index.html', cart_items=cart_items, addresses=addresses)


@blueprint.route('/', methods=['POST'])
def add():
    """Add items to cart"""
    data = request.get_json()
    product_sku = ProductSku.query.filter_by(id=data['sku_id']).first()
    amount = int(data['amount'])
    try:
        product_sku.can_add_to_cart(amount)
    except Exception as e:
        return Response(e.args, status=422)
    exist_item = UserCart.query.filter(
        and_(UserCart.user == current_user, UserCart.product_sku == product_sku)).first()
    if exist_item:
        exist_item.amount += amount
        UserCart.update(exist_item)
    else:
        UserCart.create(
            user=current_user,
            product_sku=product_sku,
            amount=amount
        )
    return Response(status=200)


@blueprint.route('/<id>', methods=['DELETE'])
def destroy(id):
    """Delete an item of a user`s cart"""
    cart = UserCart.query.filter_by(id=id).first()
    if cart in current_user.cart_items:
        UserCart.delete(cart)
    return Response(status=200)
