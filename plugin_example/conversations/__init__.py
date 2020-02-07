from pluggy import HookimplMarker
from flask import Blueprint, render_template

from .models import Message


hookimpl = HookimplMarker("flaskshop")

conversations_bp = Blueprint("conversations_bp", __name__, template_folder="templates")


@hookimpl
def flaskshop_load_blueprints(app):
    app.register_blueprint(conversations_bp, url_prefix="/conversations")


@conversations_bp.route("/hello")
def hello():
    return render_template("message_layout.html")
