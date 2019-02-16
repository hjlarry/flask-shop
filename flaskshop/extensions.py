from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
import flask_whooshalchemyplus

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
bootstrap = Bootstrap()

