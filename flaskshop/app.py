# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from flaskshop import commands, public, account, product, order, checkout, admin, api
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
    bootstrap
)
from flaskshop.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_global_varibles(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

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
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(account.views.blueprint)
    app.register_blueprint(product.views.blueprint)
    app.register_blueprint(order.views.blueprint)
    app.register_blueprint(checkout.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(api.api.blueprint)
    return None


def register_global_varibles(app):
    """Register global varibles for jinja2"""
    from flaskshop.public.models import Site
    from flask import request
    from urllib.parse import urlencode

    @app.context_processor
    def inject_param():
        site = Site.query.first()
        return dict(site=site)

    def get_sort_by_url(field, descending=False):
        request_get = request.args.copy()
        if descending:
            request_get['sort_by'] = '-' + field
        else:
            request_get['sort_by'] = field
        return '%s?%s' % (request.path, urlencode(request_get))

    app.add_template_global(get_sort_by_url, 'get_sort_by_url')

    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": account.models.User, "Product": product.models.Product,
                "CouponCode": checkout.models.CouponCode}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.seed)
