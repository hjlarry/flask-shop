from flask import Blueprint, render_template

from .models import Order

blueprint = Blueprint('order', __name__, url_prefix='/orders', static_folder='../static')


@blueprint.route('/')
def orders():
    """List orders."""
    return render_template('users/members.html')