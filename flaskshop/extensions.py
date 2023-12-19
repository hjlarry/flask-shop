from datetime import datetime

import arrow
from flask import abort, request, session
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import Column, DateTime, Integer, event

from flaskshop.corelib.db import PropsMixin

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate(compare_type=True)
debug_toolbar = DebugToolbarExtension()
bootstrap = Bootstrap5()
babel = Babel()


def get_locale():
    if request.args.get("lang"):
        session["lang"] = request.args.get("lang")
    return session.get("lang", "en")


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


db = SQLAlchemy(model_class=BaseModel)
