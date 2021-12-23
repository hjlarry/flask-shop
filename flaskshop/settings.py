# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from pathlib import Path

class LocalConfig:
    db_type = os.getenv('DB_TYPE', 'mysql')
    user = os.getenv('DB_USER', 'root')
    passwd = os.getenv('DB_PASSWD', '123456')
    host = os.getenv('DB_HOST', '127.0.0.1')
    port = os.getenv('DB_PORT', 3306)
    db_name = os.getenv('DB_NAME', 'flaskshop')
    if db_type == 'postgresql':
        db_uri = 'postgresql://{user}:{passwd}@{host}:{port}/{db_name}'.format(
            user=user, passwd=passwd, host=host, port=port, db_name=db_name)
    elif db_type == u'mysql':
        db_uri = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8mb4".format(
            user=user,passwd=passwd, host=host, port=port, db_name=db_name)
    redis_uri = "redis://localhost:6379"
    esearch_uri = "localhost"


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "thisisashop")

    # Redis
    # if redis is enabled, it can be used for:
    #   - cache
    #   - save product description
    #   - save page content
    USE_REDIS = False
    REDIS_URL = os.getenv("REDIS_URI", LocalConfig.redis_uri)

    # Elasticsearch
    # if elasticsearch is enabled, the home page will have a search bar
    # and while add a product, the search index will get update
    USE_ES = False
    ES_HOSTS = [
        os.getenv("ESEARCH_URI", LocalConfig.esearch_uri),
    ]

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", LocalConfig.db_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_QUERY_TIMEOUT = 0.1  # log the slow database query, and unit is second
    SQLALCHEMY_RECORD_QUERIES = True

    # Dir
    APP_DIR = Path(__file__).parent  # This directory
    PROJECT_ROOT = APP_DIR.parent
    STATIC_DIR = APP_DIR / "static"
    UPLOAD_FOLDER = "upload"
    UPLOAD_DIR = STATIC_DIR / UPLOAD_FOLDER
    DASHBOARD_TEMPLATE_FOLDER = APP_DIR / "templates" / "dashboard"
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/placeholders')

    PURCHASE_URI = os.getenv('PURCHASE_URI', '')

    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = os.getenv("FLASK_DEBUG", False)  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True

    MESSAGE_QUOTA = 10

    LANGUAGES = {
        'en': 'English',
        'bg': 'Български'
    }
    BABEL_DEFAULT_LOCALE = os.getenv('BABEL_DEFAULT_LOCALE', 'en_US')
    BABEL_DEFAULT_TIMEZONE = os.getenv('BABEL_DEFAULT_TIMEZONE', 'UTC')
    BABEL_TRANSLATION_DIRECTORIES = os.getenv('BABEL_TRANSLATION_DIRECTORIES', '../translations')
    BABEL_CURRENCY = os.getenv('BABEL_CURRENCY', 'USD')

    MAIL_SERVER = os.getenv("MAIL_SERVER", 'localhost')
    MAIL_PORT = os.getenv("MAIL_PORT", 25)
    MAIL_TLS = os.getenv("MAIL_TLS", True)
    if MAIL_TLS:
        MAIL_USE_TLS = True
        MAIL_USE_SSL = False
    else:
        MAIL_USE_TLS = False
        MAIL_USE_SSL = True
    MAIL_DEBUG = DEBUG_TB_ENABLED
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", '')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", '')
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", '')
    GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", '')

