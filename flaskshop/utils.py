# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import get_debug_queries
from flask import flash, request
from urllib.parse import urlencode

from flaskshop.public.models import Site


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def log_slow_queries(app):
    formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d}\n%(levelname)s - %(message)s")
    handler = RotatingFileHandler("slow_queries.log", maxBytes=10000000, backupCount=10)
    handler.setLevel(logging.WARN)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
                app.logger.warn(f"Context: {query.context}\n"
                                f"SLOW QUERY: {query.statement}\n"
                                f"Parameters: {query.parameters}\n"
                                f"Duration: {query.duration}")
        return response


def jinja_global_varibles(app):
    """Register global varibles for jinja2"""

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
        return f'{request.path}?{urlencode(request_get)}'

    app.add_template_global(get_sort_by_url, 'get_sort_by_url')

    return None
