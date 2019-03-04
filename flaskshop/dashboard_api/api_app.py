from flask import request
from flask.views import MethodView

from flaskshop.extensions import db
from flaskshop.settings import ProdConfig
from .utils import ApiFlask


def create_app():
    app = ApiFlask(__name__)
    app.config.from_object(ProdConfig)
    db.init_app(app)
    return app


json_api = create_app()


def user_del(id):
    print(id)


def user(id):
    print(id)


json_api.add_url_rule("/users/<int:id>/delete", view_func=user_del, methods=["DELETE"])
json_api.add_url_rule("/users/<int:id>", view_func=user)

