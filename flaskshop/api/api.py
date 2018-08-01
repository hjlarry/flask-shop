from flask import Blueprint
from flask_restplus import Api

from .product import api as product_api

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='Saleor API',
    description='A simple API',
)
api.add_namespace(product_api)