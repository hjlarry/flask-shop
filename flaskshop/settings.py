# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from pathlib import Path


class LocalConfig:
    db_uri = "mysql+pymysql://root:root@127.0.0.1:3306/flaskshop?charset=utf8mb4"
    redis_uri = "redis://localhost:6379"
    esearch_uri = "localhost"


class Config(object):
    """Base configuration."""

    SECRET_KEY = "thisisashop"


    APP_DIR = Path(__file__).parent  # This directory
    PROJECT_ROOT = APP_DIR.parent
    STATIC_DIR = APP_DIR / "static"
    UPLOAD_FOLDER = "upload"
    UPLOAD_DIR = STATIC_DIR / UPLOAD_FOLDER
    DASHBOARD_TEMPLATE_FOLDER = APP_DIR / "templates" / "dashboard"

    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_QUERY_TIMEOUT = 0.1  # log the slow database query, and unit is second
    SQLALCHEMY_RECORD_QUERIES = True

    # try to get config from docker-compose.yml
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", LocalConfig.db_uri)
    REDIS_URL = os.getenv("REDIS_URI", LocalConfig.redis_uri)
    ES_HOSTS = [
        os.getenv("ESEARCH_URI", LocalConfig.esearch_uri),
    ]

    MESSAGE_QUOTA = 10


class ProdConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/example"
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    PURCHASE_URI = "https://openapi.alipaydev.com/gateway.do?"
    DEBUG_TB_ENABLED = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/test"
    BCRYPT_LOG_ROUNDS = (
        4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    )
    WTF_CSRF_ENABLED = False  # Allows form testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False
