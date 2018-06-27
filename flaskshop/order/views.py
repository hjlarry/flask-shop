from flask import Blueprint, render_template, request
from flask_login import login_required

from .models import Order

blueprint = Blueprint('order', __name__, url_prefix='/orders', static_folder='../static')


@blueprint.before_request
@login_required
def before_request():
    """The whole blueprint need to login first"""
    pass


@blueprint.route('/')
def index():
    """List orders."""
    return render_template('users/members.html')


@blueprint.route('/<id>')
def show(id):
    """Show an order."""
    return render_template('users/members.html')


@blueprint.route('/', methods=['POST'])
def store():
    data = request.get_json()
    Order.create()
