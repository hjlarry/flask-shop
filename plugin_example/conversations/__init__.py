from pluggy import HookimplMarker
from flask import render_template
from flask_login import current_user

from .views import conversations_bp
from .utils import get_unread_count, get_latest_messages

hookimpl = HookimplMarker("flaskshop")


@hookimpl
def flaskbb_tpl_user_nav_loggedin_before():
    return render_template(
        "_inject_navlink.html",
        unread_messages=get_latest_messages(current_user),
        unread_count=get_unread_count(current_user),
    )


@hookimpl
def flaskshop_load_blueprints(app):
    app.register_blueprint(conversations_bp, url_prefix="/conversations")
