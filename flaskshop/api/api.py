from flask import Blueprint, request, Response
from flask_restplus import Api
from flaskshop.extensions import csrf_protect

from .product import api as product_api
from .auth import api as auth_api
from .auth import CustomSessionInterface

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
csrf_protect.exempt(blueprint)
blueprint.session_interface = CustomSessionInterface()
ALLOWED_PATHS = frozenset(['/api/v1/user/login', ])


@blueprint.after_request
def verify_user(response):
    from .auth import verify_token
    if request.path in ALLOWED_PATHS or request.method == 'OPTIONS':
        return response
    elif 'Authorization' in request.headers:
        data = verify_token(request.headers['Authorization'])
        if data:
            return response
    return Response(status=401)


api = Api(blueprint, version="1.0", title="Saleor API", description="A simple API")


@api.errorhandler
def default_error_handler(error):
    """Default error handler"""
    return {"message": str(error)}, getattr(error, "code", 500)


api.add_namespace(product_api)
api.add_namespace(auth_api)
