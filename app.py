# -*- coding: utf-8 -*-
"""Create an application instance."""
from flaskshop.app import create_app

app = create_app()

app.run('127.0.0.1','3000')