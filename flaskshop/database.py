import datetime

from flaskshop.corelib.mc import cache, rdb
from .extensions import db

Column = db.Column
MC_KEY_GET_BY_ID = "global:{}:{}"


class CRUDMixin:
    @classmethod
    def create(cls, **kwargs):
        props = cls.get_db_props(kwargs)
        obj = cls(**kwargs)
        obj.save()
        cls.update_db_props(obj, props)
        return obj

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    @cache(MC_KEY_GET_BY_ID.format("{cls.__name__}", "{record_id}"))
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None

    @classmethod
    def get_or_create(cls, **kwargs):
        props = cls.get_db_props(kwargs)
        if not kwargs:
            return None, False
        obj = cls.query.filter_by(**kwargs).first()
        if obj:
            return obj, False
        obj = cls(**kwargs)
        obj.save()
        cls.update_db_props(obj, props)
        return obj, True

    @classmethod
    def create_or_update(cls, **kwargs):
        session = db.session
        props = cls.get_db_props(kwargs)
        id = kwargs.pop("id", None)
        if id is not None:
            obj = cls.query.get(id)
            if obj:
                if "updated_at" not in kwargs:
                    kwargs["updated_at"] = datetime.now()
                for k, v in kwargs.items():
                    setattr(obj, k, v)
                session.commit()
                cls.update_db_props(obj, props)
                return obj, False
        obj = cls(**kwargs)
        obj.save()
        cls.update_db_props(obj, props)
        return obj, True

    @classmethod
    def get_db_props(cls, kwargs):
        props = {}
        for col, default in cls._db_columns:
            props[col] = kwargs.pop(col, default)
        return props

    @classmethod
    def update_db_props(cls, obj, db_props):
        for prop, value in db_props.items():
            obj.set_props_item(prop, value)

    @classmethod
    def __flush_after_update_event__(cls, target):
        rdb.delete(MC_KEY_GET_BY_ID.format(cls.__name__, target.id))

    @classmethod
    def __flush_delete_event__(cls, target):
        rdb.delete(MC_KEY_GET_BY_ID.format(cls.__name__, target.id))


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True
