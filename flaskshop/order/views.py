from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.wrappers import Response
import uuid
import json

from .models import Order, OrderItem
from flaskshop.user.models import UserAddress
from flaskshop.cart.models import UserCart

blueprint = Blueprint('order', __name__, url_prefix='/orders', static_folder='../static')


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route('/')
def index():
    """List orders."""
    page = request.args.get("page", 1, type=int)
    pagination = current_user.orders.paginate(page, per_page=16)
    orders = pagination.items
    return render_template('orders/index.html', orders=orders, pagination=pagination)


@blueprint.route('/<id>')
def show(id):
    """Show an order."""
    order = Order.query.filter_by(id=id).first()
    return render_template('orders/show.html', order=order)


@blueprint.route('/', methods=['POST'])
def store():
    data = request.get_json()
    address = UserAddress.query.filter_by(id=data['address_id']).first()
    total_amount = 0
    items = []
    for item in data['items']:
        cart_item = UserCart.query.filter_by(id=item['item_id']).first()
        amount = int(item['amount'])
        try:
            cart_item.product_sku.decrement_stock(amount)
        except Exception as e:
            return Response(e.args, status=422)
        order_item = OrderItem(
            product_sku=cart_item.product_sku,
            product=cart_item.product_sku.product,
            amount=amount,
            price=amount * cart_item.product_sku.price
        )
        total_amount += order_item.price
        cart_item.release(amount)
        items.append(order_item)

    if not items:
        return Response('Need choose an item first', status=422)
    order = Order.create(
        user=current_user,
        no=str(uuid.uuid1()),
        address=address.full_address + address.contact_name + address.contact_phone,
        remark=data['remark'],
        total_amount=total_amount,
        items=items
    )
    res = {'id': order.id}

    return Response(json.dumps(res), status=200, mimetype='application/json')
