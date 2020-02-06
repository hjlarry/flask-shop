from flask import Blueprint, request
from flask_restplus import Api
from pluggy import HookimplMarker

from flaskshop.extensions import csrf_protect

from .product import api as product_api
from .checkout import api as checkout_api
from .auth import api as auth_api
from .auth import CustomSessionInterface

impl = HookimplMarker("flaskshop")


@impl
def flaskshop_load_blueprints(app):
    bp = Blueprint("api", __name__)

    csrf_protect.exempt(bp)
    bp.session_interface = CustomSessionInterface()
    ALLOWED_PATHS = frozenset(
        ["/api/v1/user/login", "/api/v1/", "/api/v1/swagger.json", "/api/v1/products/"]
    )

    @bp.after_request
    def verify_user(response):
        from .auth import verify_token

        if request.path in ALLOWED_PATHS or request.method == "OPTIONS":
            return response
        elif "Authorization" in request.headers:
            data = verify_token(request.headers["Authorization"])
            if data:
                return response
        return "", 401

    api = Api(bp, version="1.0", title="Saleor API", description="A simple API")

    @api.errorhandler
    def default_error_handler(error):
        """Default error handler"""
        return {"message": str(error)}, getattr(error, "code", 500)

    api.add_namespace(product_api)
    api.add_namespace(checkout_api)
    api.add_namespace(auth_api)

    app.register_blueprint(bp, url_prefix="/api/v1")
