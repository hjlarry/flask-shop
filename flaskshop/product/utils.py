from flask import request
from flask_login import current_user
from sqlalchemy import desc

from flaskshop.checkout.models import Cart, CartLine


def get_name_from_attributes(variant):
    """Generates ProductVariant's name based on its attributes."""
    attributes = variant.product.product_type.variant_attributes
    values = get_attributes_display_map(variant, attributes)
    return generate_name_from_values(values)


def generate_name_from_values(attributes_dict):
    """Generates name from AttributeChoiceValues. Attributes dict is sorted,
    as attributes order should be kept within each save.

    Args:
        attributes_dict: dict of attribute_pk: AttributeChoiceValue values
    """
    return " / ".join(attributechoice_value
                      for attribute_pk, attributechoice_value in sorted(
                          attributes_dict.items(), key=lambda x: x[0]))


def add_to_currentuser_cart(quantity, variant_id):
    if current_user.cart:
        cart = current_user.cart
        cart.quantity += quantity
    else:
        cart = Cart.create(user=current_user, quantity=quantity)
    line = CartLine.query.filter_by(cart=cart, variant_id=variant_id).first()
    if line:
        quantity += line.quantity
        line.update(quantity=quantity)
    else:
        CartLine.create(variant_id=variant_id, quantity=quantity, cart=cart)
