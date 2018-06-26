from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from .models import UserCart

blueprint = Blueprint('cart', __name__, url_prefix='/cart', static_folder='../static')


@login_required
@blueprint.route('/')
def carts():
    """List cartItems."""
    cart_items = current_user.cart_items
    return render_template('cart/index.html', cart_items=cart_items)


@blueprint.route('/add', methods=['POST'])
def cart_add():
    """Add items to cart"""
    if current_user.is_authenticated:
        data = request.get_json()
        UserCart.create(
            user=current_user,
            product_sku_id=data['sku_id'],
            amount=data['amount']
        )
        return Response(status=200)
    return Response(status=401)
