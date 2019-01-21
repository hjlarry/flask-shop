from flask import request
from flask_login import current_user
from sqlalchemy import desc

from flaskshop.checkout.models import Cart, CartLine


def get_product_attributes_data(product):
    """Returns attributes associated with the product,
    as dict of ProductAttribute: AttributeChoiceValue values.
    """
    attributes = product.product_type.product_attributes
    attributes_map = {attribute.id: attribute for attribute in attributes}
    values_map = get_attributes_display_map(product, attributes)
    return {
        attributes_map.get(attr_pk): value_obj
        for (attr_pk, value_obj) in values_map.items()
    }


def get_name_from_attributes(variant):
    """Generates ProductVariant's name based on its attributes."""
    attributes = variant.product.product_type.variant_attributes
    values = get_attributes_display_map(variant, attributes)
    return generate_name_from_values(values)


def get_attributes_display_map(obj, attributes):
    """Returns attributes associated with an object,
    as dict of ProductAttribute: AttributeChoiceValue values.

    Args:
        attributes: ProductAttribute Iterable
    """
    display_map = {}
    for attribute in attributes:
        value = obj.attributes.get(str(attribute.id))
        if value:
            choices = {a.id: a for a in attribute.values}
            choice_obj = choices.get(int(value))
            if choice_obj:
                display_map[attribute.id] = choice_obj.title
            else:
                display_map[attribute.id] = value
    return display_map


def generate_name_from_values(attributes_dict):
    """Generates name from AttributeChoiceValues. Attributes dict is sorted,
    as attributes order should be kept within each save.

    Args:
        attributes_dict: dict of attribute_pk: AttributeChoiceValue values
    """
    return " / ".join(attributechoice_value
                      for attribute_pk, attributechoice_value in sorted(
                          attributes_dict.items(), key=lambda x: x[0]))


def get_product_list_context(products):
    from .models import Product

    args_dict = {}

    price_from = request.args.get("price_from", None, type=int)
    price_to = request.args.get("price_to", None, type=int)
    if price_from:
        products = products.filter(Product.price > price_from)
    if price_to:
        products = products.filter(Product.price < price_to)
    args_dict.update(price_from=price_from, price_to=price_to)

    sort_by_choices = {"title": "title", "price": "price"}
    arg_sort_by = request.args.get("sort_by", "")
    is_descending = False
    if arg_sort_by.startswith("-"):
        is_descending = True
        arg_sort_by = arg_sort_by[1:]
    if arg_sort_by in sort_by_choices:
        products = (products.order_by(desc(getattr(Product, arg_sort_by)))
                    if is_descending else products.order_by(
                        getattr(Product, arg_sort_by)))
    now_sorted_by = arg_sort_by or "title"
    args_dict.update(
        sort_by_choices=sort_by_choices,
        now_sorted_by=now_sorted_by,
        is_descending=is_descending,
    )

    args_dict.update(default_attr={})
    attr_filter = set()
    for product in products:
        for attr in product.product_type.product_attributes:
            attr_filter.add(attr)
    for attr in attr_filter:
        value = request.args.get(attr.title)
        if value:
            products = products.filter(
                Product.attributes.__getitem__(str(attr.id)) == value)
            args_dict["default_attr"].update({attr.title: int(value)})
    args_dict.update(attr_filter=attr_filter)

    if request.args:
        args_dict.update(clear_filter=True)

    return args_dict, products


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
