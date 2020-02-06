from flask import Blueprint
from pluggy import HookimplMarker

from .models import *

impl = HookimplMarker("flaskshop")


def hello():
    return "787"


@impl
def flaskshop_load_blueprints(app):
    discount = Blueprint("discount", __name__)
    discount.add_url_rule("/he", view_func=hello)
    app.register_blueprint(discount, url_prefix="/discount")
