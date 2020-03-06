from datetime import datetime

from flask import abort
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, Model, BaseQuery, DefaultMeta, _QueryProperty
from sqlalchemy import Column, Integer, DateTime, event
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
import arrow

from flaskshop.corelib.db import PropsItem, PropsMixin

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate(compare_type=True)
debug_toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()


class BaseModel(PropsMixin, Model):
    __table_args__ = {"mysql_charset": "utf8mb4", "extend_existing": True}
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id}>"

    def get_uuid(self):
        return f"/bran/{self.__class__.__name__}/{self.id}"

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        rv = cls.get(id)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(id) for id in ids]

    def url(self):
        return f"/{self.__class__.__name__.lower()}/{self.id}"

    def to_dict(self):
        columns = self.__table__.columns.keys() + ["kind"]
        return {key: getattr(self, key, None) for key in columns}

    @property
    def created_at_human(self):
        return arrow.get(self.created_at).humanize()

    @staticmethod
    def _flush_event(mapper, connection, target):
        target.__flush_event__(target)

    @classmethod
    def __flush_event__(cls, target):
        pass

    @staticmethod
    def _flush_insert_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_insert_event__(target)

    @staticmethod
    def _flush_before_update_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_before_update_event__(target)

    @staticmethod
    def _flush_after_update_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_after_update_event__(target)

    @staticmethod
    def _flush_delete_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_delete_event__(target)

    @classmethod
    def __flush_insert_event__(cls, target):
        pass

    @classmethod
    def __flush_before_update_event__(cls, target):
        pass

    @classmethod
    def __flush_after_update_event__(cls, target):
        pass

    @classmethod
    def __flush_delete_event__(cls, target):
        pass

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "after_insert", cls._flush_insert_event)
        event.listen(cls, "before_update", cls._flush_before_update_event)
        event.listen(cls, "after_update", cls._flush_after_update_event)
        event.listen(cls, "after_delete", cls._flush_delete_event)


class BindDBPropertyMixin:
    def __init__(cls, name, bases, d):
        super().__init__(name, bases, d)
        db_columns = []
        for k, v in d.items():
            if isinstance(v, PropsItem):
                db_columns.append((k, v.default))
        setattr(cls, "_db_columns", db_columns)


class CombinedMeta(BindDBPropertyMixin, DefaultMeta):
    pass


class UnLockedAlchemy(SQLAlchemy):
    def make_declarative_base(self, model, metadata=None):
        if not isinstance(model, DeclarativeMeta):
            model = declarative_base(
                cls=model, name="Model", metadata=metadata, metaclass=CombinedMeta
            )
        if metadata is not None and model.metadata is not metadata:
            model.metadata = metadata

        if not getattr(model, "query_class", None):
            model.query_class = self.Query

        model.query = _QueryProperty(self)
        return model

    def apply_driver_hacks(self, app, info, options):
        if "isolation_level" not in options:
            options["isolation_level"] = "READ COMMITTED"
        return super().apply_driver_hacks(app, info, options)


db = UnLockedAlchemy(model_class=BaseModel)
