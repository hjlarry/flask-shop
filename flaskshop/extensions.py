import hashlib
import functools
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, Model, BaseQuery, DefaultMeta, _QueryProperty
from dogpile.cache import make_region
from dogpile.cache.api import NO_VALUE
from sqlalchemy import Column, Integer, DateTime, event, inspect
from sqlalchemy.ext.declarative import declared_attr, DeclarativeMeta, declarative_base
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.orm.interfaces import MapperOption

from flaskshop.corelib.db import PropsItem, PropsMixin
from flaskshop.settings import REDIS_URL

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate(compare_type=True)
debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
bootstrap = Bootstrap()


def md5_key_mangler(key):
    if key.startswith("SELECT "):
        key = hashlib.md5(key.encode("ascii")).hexdigest()
    return key


regions = dict(
    default=make_region(key_mangler=md5_key_mangler).configure("dogpile.cache.redis"),
    arguments={"url": REDIS_URL},
)


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


class CachingQuery(BaseQuery):
    def __init__(self, regions, entities, *args, **kwargs):
        self.cache_regions = regions
        super().__init__(entities=entities, *args, **kwargs)

    def __iter__(self):
        if hasattr(self, "_cache_region"):
            return self.get_value(createfunc=lambda: list(BaseQuery.__iter__(self)))
        else:
            return BaseQuery.__iter__(self)

    def _get_cache_plus_key(self):
        dogpile_region = self.cache_regions[self._cache_region.region]
        if self._cache_region.cache_key:
            key = self._cache_region.cache_key
        else:
            key = _key_from_query(self)
        return dogpile_region, key

    def invalidate(self):
        dogpile_region, cache_key = self._get_cache_plus_key()
        dogpile_region.delete(cache_key)

    def get_value(
        self, merge=True, createfunc=None, expiration_time=None, ignore_expiration=False
    ):
        dogpile_region, cache_key = self._get_cache_plus_key()
        assert (
            not ignore_expiration or not createfunc
        ), "can`t ignore expiration and also provide createfunc"
        if ignore_expiration or not createfunc:
            cached_value = dogpile_region.get(
                cache_key,
                expiration_time=expiration_time,
                ignore_expiration=ignore_expiration,
            )
        else:
            cached_value = dogpile_region.get_or_create(
                cache_key, createfunc, expiration_time=expiration_time
            )
        if cached_value is NO_VALUE:
            raise KeyError(cache_key)
        if merge:
            cached_value = self.merge_result(cached_value, load=False)
        return cached_value

    def set_value(self, value):
        dogpile_region, cache_key = self._get_cache_plus_key()
        dogpile_region.set(cache_key, value)


def query_callable(regions, query_cls=CachingQuery):
    return functools.partial(query_cls, regions)


class FromCache(MapperOption):
    propagate_to_loaders = False

    def __init__(self, region="default", cache_key=None):
        self.region = region
        self.cache_key = cache_key

    def process_query(self, query):
        query._cache_region = self


class Cache:
    def __init__(self, model, regions, label):
        self.model = model
        self.regions = regions
        self.label = label
        self.pk = getattr(model, "cache_pk", "id")

    def get(self, pk):
        return self.model.query.options(self.from_cache(pk=pk)).get(pk)

    def count(self, **kwargs):
        if kwargs:
            if len(kwargs) > 1:
                raise TypeError("filter accept only one attribute for filtering")
            key, value = list(kwargs.items())[0]
            if key not in self._attrs():
                raise TypeError(f"{self} does not have an attribute {key}")
        cache_key = self._count_cache_key(**kwargs)
        r = self.regions[self.label]
        count = r.get(cache_key)
        if count is NO_VALUE:
            count = self.model.query.filter_by(**kwargs).count()
            r.set(cache_key, count)
        return count

    def filter(self, order_by="asc", offset=None, limit=None, **kwargs):
        if kwargs:
            if len(kwargs) > 1:
                raise TypeError("filter accept only one attribute for filtering")
            key, value = list(kwargs.items())[0]
            if key not in self._attrs():
                raise TypeError(f"{self} does not have an attribute {key}")
        cache_key = self._cache_key(**kwargs)
        r = self.regions[self.label]
        pks = r.get(cache_key)
        if pks is NO_VALUE:
            pks = [
                o.id
                for o in self.model.query.filter_by(**kwargs).with_entities(
                    getattr(self.model, self.pk)
                )
            ]
            r.set(cache_key, pks)
        if order_by == "desc":
            pks.reverse()
        if offset is not None:
            pks = pks[offset:]
        if limit is not None:
            pks = pks[:limit]
        keys = [self._cache_key(id) for id in pks]
        return Query(self.get_entities(pks, r.get_multi(keys)))

    def get_entities(self, pks, objs):
        for pos, obj in enumerate(objs):
            if obj is NO_VALUE:
                yield self.get(pks[pos])
            else:
                yield obj[0]

    def flush(self, key):
        self.regions[self.label].delete(key)

    @memoize
    def _attrs(self):
        return [a.key for a in inspect(self.model).attrs if a.key != self.pk]

    @memoize
    def from_cache(self, cache_key=None, pk=None):
        if pk:
            cache_key = self._cache_key(pk)
        return FromCache(self.label, cache_key)

    @memoize
    def _count_cache_key(self, pk="all", **kwargs):
        return self._cache_key(pk, **kwargs) + "_count"

    @memoize
    def _cache_key(self, pk="all", **kwargs):
        q_filter = "".join(f"{k}={v}" for k, v in kwargs.items()) or self.pk
        return f"{self.model.__tablename__}.{q_filter}[{pk}]"

    def _flush_all(self, obj):
        for attr in self._attrs():
            added, unchanged, deleted = get_history(obj, attr)
            for value in list(deleted) + list(added):
                self.flush(self._cache_key(**{attr: value}))
        for key in (
            self._cache_key(),
            self._cache_key(getattr(obj, self.pk)),
            self._count_cache_key(),
            self._count_cache_key(getattr(obj, self.pk)),
        ):
            self.flush(key)


class BaseModel(PropsMixin, Model):
    cache_label = "default"
    cache_regions = regions
    query_class = query_callable(regions)

    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=None)

    def get_uuid(self):
        return f"/bran/{self.__class__.__name__}/{self.id}"

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id}>"

    @declared_attr
    def cache(cls):
        return Cache(cls, cls.cache_regions, cls.cache_label)

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

    @staticmethod
    def _flush_event(mapper, connection, target):
        target.cache._flush_all(target)
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

