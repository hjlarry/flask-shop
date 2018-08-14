from flask import Blueprint

from .models import *

blueprint = Blueprint('discount', __name__, url_prefix='/discount')