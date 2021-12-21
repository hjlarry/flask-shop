from flask import Blueprint
from pluggy import HookimplMarker

from .models import *

impl = HookimplMarker("flaskshop")


@impl
def flaskshop_load_blueprints(app):
    discount = Blueprint("discount", __name__)
    app.register_blueprint(discount, url_prefix="/discount")
