from pluggy import HookimplMarker

from .views import conversations_bp

hookimpl = HookimplMarker("flaskshop")


@hookimpl
def flaskshop_load_blueprints(app):
    app.register_blueprint(conversations_bp, url_prefix="/conversations")



