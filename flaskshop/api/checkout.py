from flask_restplus import Namespace, Resource, fields
from flask_login import current_user
from flask_babel import lazy_gettext

api = Namespace("checkout", description=lazy_gettext("Checkout related operations"))

cart = api.model(
    "CartLine",
    {
        "id": fields.Integer(required=True, description=lazy_gettext("The checkout cartline id")),
        "quantity": fields.Integer(required=True, description=lazy_gettext("The cart item num")),
        "title": fields.String(
            description=lazy_gettext("The cart item title"), attribute="variant.product.title"
        ),
        "variant": fields.String(
            description=lazy_gettext("The cart item variant"), attribute="variant.title"
        ),
        "product_id": fields.Integer(
            description=lazy_gettext("The cart item product"), attribute="variant.product.id"
        ),
        "price": fields.Float(
            description=lazy_gettext("The cart item price"), attribute="variant.price"
        ),
        "first_img": fields.String(
            description=lazy_gettext("The cart item image"), attribute="variant.product.first_img"
        ),
    },
)


@api.route("/cart")
class CartIndex(Resource):
    @api.doc("list_products")
    @api.marshal_list_with(cart)
    def get(self):
        """List current user cart items"""
        cartitems = current_user.cart.lines
        return cartitems
