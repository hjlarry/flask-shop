# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get("FLASKSHOP_SECRET", "thisisashop")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEBPACK_MANIFEST_PATH = "webpack/manifest.json"


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/example"
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flaskshop"
    PURCHASE_URI = "https://openapi.alipaydev.com/gateway.do?"
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    BCRYPT_LOG_ROUNDS = (
        4
    )  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
