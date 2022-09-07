# -*- coding: utf-8 -*-
"""Test configs."""
from flaskshop.app import create_app
from flaskshop.settings import Config, ProdConfig


def test_production_config():
    """Production config."""
    app = create_app(ProdConfig)
    assert app.config["ENV"] == "prod"
    assert app.config["FLASK_DEBUG"] is False
    assert app.config["DEBUG_TB_ENABLED"] is False


def test_dev_config():
    """Development config."""
    app = create_app(Config)
    assert app.config["ENV"] == "dev"
    assert app.config["FLASK_DEBUG"] is True
