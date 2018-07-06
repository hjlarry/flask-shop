# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin, AdminIndexView

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cache = Cache()
debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
admin_manager = Admin(
    index_view=AdminIndexView(menu_icon_type='fa', menu_icon_value='fa-home nav-icon'),
    base_template='adminlte.html',
    template_mode='bootstrap3',
    category_icon_classes={'Products': 'fa fa-product-hunt nav-icon', 'Users': 'fa fa-users nav-icon'}

)
