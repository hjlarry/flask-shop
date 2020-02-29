from flaskshop.database import Column, Model, db

class PluginRegistry(Model):
    __tablename__ = "plugin_registry"
    name = Column(db.String(100), unique=True)
    enabled = Column(db.Boolean(), default=True)
