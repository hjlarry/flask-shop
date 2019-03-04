# -*- coding: utf-8 -*-
"""Create an application instance."""
import os

from flaskshop.app import create_app
from flaskshop import settings

config = getattr(settings, os.environ.get("CURRENT_CONFIG"), "ProdConfig")
app = create_app(config)
