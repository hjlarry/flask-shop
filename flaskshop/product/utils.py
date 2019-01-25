from flask import request
from flask_login import current_user
from sqlalchemy import desc

from flaskshop.checkout.models import Cart, CartLine


def get_name_from_attributes(variant):
    """Generates ProductVariant's name based on its attributes."""
    values = [
        attributechoice_value.title
        for attributechoice_value in variant.attribute_map.values()
    ]
    return " / ".join(values)


def add_to_currentuser_cart(quantity, variant_id):
    cart = Cart.get_by_user_id(current_user.id)
    if cart:
        cart.quantity += quantity
        cart.save()
    else:
        cart = Cart.create(user_id=current_user.id, quantity=quantity)
    line = CartLine.query.filter_by(cart=cart, variant_id=variant_id).first()
    if line:
        quantity += line.quantity
        line.update(quantity=quantity)
    else:
        CartLine.create(variant_id=variant_id, quantity=quantity, cart=cart)
