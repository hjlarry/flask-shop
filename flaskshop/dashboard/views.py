from functools import wraps
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(401)
        return func(*args, **kwargs)

    return decorated_view


@blueprint.before_request
@admin_required
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route("/")
def index():
    return render_template("dashboard/index.html")

