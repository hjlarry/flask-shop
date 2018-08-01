from flask_restplus import Namespace, Resource, fields
from flaskshop.product.models import Product

api = Namespace('products', description='Products related operations')

product = api.model('Product', {
    'id': fields.String(required=True, description='The product identifier'),
    'title': fields.String(required=True, description='The product name'),
    'description': fields.String(required=True, description='The product description'),
    'first_img': fields.String(required=True, description='The product img'),
})


@api.route('/')
class CatList(Resource):
    @api.doc('list_products')
    @api.marshal_list_with(product)
    def get(self):
        """List all products"""
        products = Product.query.filter_by(is_featured=True).limit(8)
        return [p.to_dict() for p in products]


@api.route('/<id>')
@api.param('id', 'The product identifier')
@api.response(404, 'Product not found')
class Cat(Resource):
    @api.doc('get_cat')
    @api.marshal_with(product)
    def get(self, id):
        """Fetch a product """
        product = Product.query.get(id)
        if product:
            return product
        api.abort(404)
