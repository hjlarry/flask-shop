# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from flaskshop import (
    commands,
    public,
    account,
    product,
    order,
    checkout,
    admin,
    api,
    discount,
    dashboard,
)
from flaskshop.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
    webpack,
    admin_manager,
    bootstrap,
    flask_whooshalchemyplus,
)
from flaskshop.settings import ProdConfig
from flaskshop.utils import log_slow_queries, jinja_global_varibles


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    jinja_global_varibles(app)
    log_slow_queries(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)
    admin_manager.init_app(app)
    bootstrap.init_app(app)
    flask_whooshalchemyplus.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(account.views.blueprint)
    app.register_blueprint(product.views.blueprint)
    app.register_blueprint(order.views.blueprint)
    app.register_blueprint(checkout.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(discount.views.blueprint)
    app.register_blueprint(api.api.blueprint)
    app.register_blueprint(dashboard.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"errors/{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            "User": account.models.User,
            "Product": product.models.Product,
            "Order": order.models.Order,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.seed)
    app.cli.add_command(commands.search_index)
