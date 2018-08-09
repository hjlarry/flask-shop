from flask_restplus import Namespace, Resource, fields
from flask import request
from flask_login import current_user


api = Namespace('checkout', description='Checkout related operations')

cart = api.model('CartLine', {
    'id': fields.Integer(required=True, description='The checkout cartline id'),
    'quantity': fields.Integer(required=True, description='The cart item num'),
    'title': fields.String(description='The cart item num', attribute='variant.product.title'),
    'variant': fields.String(description='The cart item num', attribute='variant.title'),
    'product_id': fields.Integer(description='The cart item num', attribute='variant.product.id'),
    'price': fields.String(description='The cart item num', attribute='variant.price'),
    'first_img': fields.String(description='The cart item num', attribute='variant.product.get_first_img'),
})


@api.route('/cart')
class CartIndex(Resource):
    @api.doc('list_products')
    @api.marshal_list_with(cart)
    def get(self):
        """List current user cart items"""
        cartitems = current_user.cart.lines
        return cartitems
