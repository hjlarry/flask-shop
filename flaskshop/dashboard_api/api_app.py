import os

from flask import request
from flask.views import MethodView

from flaskshop.extensions import db
from flaskshop import settings
from .utils import ApiFlask


def create_app(config):
    app = ApiFlask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app


config = getattr(settings, os.environ.get("CURRENT_CONFIG"), "ProdConfig")
json_api = create_app(config)


def user_del(id):
    print(id)


def user(id):
    print(id)


json_api.add_url_rule("/users/<int:id>/delete", view_func=user_del, methods=["DELETE"])
json_api.add_url_rule("/users/<int:id>", view_func=user)

