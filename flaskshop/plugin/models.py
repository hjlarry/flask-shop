from flask import current_app

from flaskshop.database import Column, Model, db


class PluginRegistry(Model):
    __tablename__ = "plugin_registry"
    name = Column(db.String(100), unique=True)
    enabled = Column(db.Boolean(), default=True)

    @property
    def info(self):
        return current_app.pluggy.plugin_metadata.get(self.name, {})
