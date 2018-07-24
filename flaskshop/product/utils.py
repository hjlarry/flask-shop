def get_product_attributes_data(product):
    """Returns attributes associated with the product,
    as dict of ProductAttribute: AttributeChoiceValue values.
    """
    attributes = product.product_type.product_attributes.all()
    attributes_map = {attribute.id: attribute for attribute in attributes}
    values_map = get_attributes_display_map(product, attributes)
    return {attributes_map.get(attr_pk): value_obj
            for (attr_pk, value_obj) in values_map.items()}


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
        value = obj.attributes.get(attribute.id)
        if value:
            choices = {a.id: a for a in attribute.values}
            choice_obj = choices.get(value)
            if choice_obj:
                display_map[attribute.id] = choice_obj
            else:
                display_map[attribute.id] = value
    return display_map


def generate_name_from_values(attributes_dict):
    """Generates name from AttributeChoiceValues. Attributes dict is sorted,
    as attributes order should be kept within each save.

    Args:
        attributes_dict: dict of attribute_pk: AttributeChoiceValue values
    """
    return ' / '.join(
        attributechoice_value
        for attribute_pk, attributechoice_value in sorted(
            attributes_dict.items(),
            key=lambda x: x[0]))
