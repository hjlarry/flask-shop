from flask_restplus import Namespace, Resource, fields
from flask import request
from flaskshop.product.models import Product

api = Namespace('products', description='Products related operations')

product = api.model('ProductList', {
    'id': fields.String(required=True, description='The product identifier'),
    'title': fields.String(required=True, description='The product name'),
    'description': fields.String(description='The product description'),
    'first_img': fields.String(description='The product first img', attribute='get_first_img'),
    'images': fields.List(fields.String, description='The product images')
})


@api.route('/')
class ProductList(Resource):
    @api.doc('list_products')
    @api.marshal_list_with(product)
    def get(self):
        """List all products"""
        page = request.args.get('page', 1, int)
        products = Product.query.paginate(page, per_page=8).items
        return products


@api.route('/<id>')
@api.param('id', 'The product identifier')
@api.response(404, 'Product not found')
class ProductDetail(Resource):
    @api.doc('get_product')
    @api.marshal_with(product)
    def get(self, id):
        """Fetch a product """
        product = Product.query.get(id)
        if product:
            return product
        api.abort(404)
