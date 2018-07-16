# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask import redirect, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cache = Cache()
debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
bootstrap = Bootstrap()


class CustomAdminIndexView(AdminIndexView):
    def __init__(self):
        super().__init__(menu_icon_value='fa-home nav-icon')

    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return True
            else:
                flash('This is not an administrator', 'warning')
                return False
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('public.login', next=request.url))


admin_manager = Admin(
    index_view=CustomAdminIndexView(),
    base_template='admin/layout.html',
    template_mode='bootstrap3'
)
