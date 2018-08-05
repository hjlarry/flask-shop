from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header
from flaskshop.extensions import login_manager


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get("login_via_header"):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


# app.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True


@login_manager.request_loader
def load_user_from_request(request):

    api_key = request.headers.get("Authorization")
    if api_key:
        api_key = api_key.replace("Basic ", "", 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None
