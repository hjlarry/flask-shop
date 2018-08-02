from flask import Blueprint
from flask_restplus import Api

from .product import api as product_api

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='Saleor API',
          description='A simple API',
          )


@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error)}, getattr(error, 'code', 500)


api.add_namespace(product_api)
