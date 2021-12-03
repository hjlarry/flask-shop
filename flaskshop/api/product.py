from flask_restplus import Namespace, Resource, fields
from flask_login import current_user
from flask import request
from flask_babel import lazy_gettext

from flaskshop.product.models import Product
from flaskshop.checkout.models import Cart

api = Namespace("products", description=lazy_gettext("Products related operations"))
parser = api.parser()
parser.add_argument("variant_id", type=int, required=True, help=lazy_gettext("The variant"))
parser.add_argument("quantity", type=int, required=True, help=lazy_gettext("The quantity"))

product_list = api.model(
    "ProductList",
    {
        "id": fields.Integer(required=True, description=lazy_gettext("The product identifier")),
        "title": fields.String(required=True, description=lazy_gettext("The product name")),
        "description": fields.String(description=lazy_gettext("The product description")),
        "price": fields.String(description=lazy_gettext("The product price")),
        "first_img": fields.String(description=lazy_gettext("The product first img")),
    },
)
variant = api.model(
    "Variant",
    {
        "id": fields.Integer(required=True, description=lazy_gettext("The variant identifier")),
        "sku": fields.String(required=True, description=lazy_gettext("The variant sku")),
        "title": fields.String(required=True, description=lazy_gettext("The variant name")),
        "price": fields.String(required=True, description=lazy_gettext("The variant price")),
        "stock": fields.String(
            required=True, description=lazy_gettext("The variant stock"), attribute="quantity"
        ),
    },
)
product_detail = api.model(
    "ProductDetail",
    {
        "id": fields.Integer(required=True, description=lazy_gettext("The product identifier")),
        "title": fields.String(required=True, description=lazy_gettext("The product name")),
        "description": fields.String(description=lazy_gettext("The product description")),
        "price": fields.String(description=lazy_gettext("The product price")),
        "images": fields.List(fields.String, description=lazy_gettext("The product images")),
        "variant": fields.List(
            fields.Nested(variant), description=lazy_gettext("The product variant")
        ),
    },
)


@api.route("/")
class ProductList(Resource):
    @api.doc("list_products")
    @api.marshal_list_with(product_list)
    def get(self):
        """List all products"""
        page = request.args.get("page", 1, int)
        products = Product.query.paginate(page, per_page=8).items
        return products


@api.route("/<int:id>")
@api.param("id", lazy_gettext("The product identifier"))
@api.response(404, lazy_gettext("Product not found"))
class ProductDetail(Resource):
    @api.doc("get_product")
    @api.marshal_with(product_detail)
    def get(self, id):
        """Fetch a product """
        product = Product.query.get(id)
        if product:
            return product
        api.abort(404)

    @api.doc(parser=parser)
    def post(self, id):
        """post product to current user cart"""
        args = parser.parse_args()
        Cart.add_to_currentuser_cart(args["quantity"], args["variant_id"])
        res = {"cart_lines": len(current_user.cart.lines)}
        return res, 201
