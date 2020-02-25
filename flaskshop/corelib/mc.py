import inspect
import functools
from pickle import UnpicklingError

from flask import request, current_app
from sqlalchemy.ext.serializer import loads, dumps

from flaskshop.corelib.db import rdb
from flaskshop.corelib.utils import Empty, empty

BUILTIN_TYPES = (int, bytes, str, float, bool)


def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults) :], defaults)) if defaults else {}

    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = key_pattern.format(*[aa[n] for n in arg_names], **aa)
        return key and key.replace(" ", "_"), aa

    return gen_key


def cache(key_pattern, expire=None):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @functools.wraps(f)
        def _(*a, **kw):
            if not current_app.config["USE_REDIS"]:
                return f(*a, **kw)
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            force = kw.pop("force", False)
            r = rdb.get(key) if not force else None
            if r is None:
                r = f(*a, **kw)
                if r is not None:
                    if not isinstance(r, BUILTIN_TYPES):
                        r = dumps(r)
                    rdb.set(key, r, expire)
                else:
                    r = dumps(empty)
                    rdb.set(key, r, expire)

            try:
                r = loads(r)
            except (TypeError, UnpicklingError):
                pass
            if isinstance(r, Empty):
                r = None
            if isinstance(r, bytes):
                r = r.decode()
            return r

        _.original_function = f
        return _

    return deco


def cache_by_args(key_pattern, expire=None):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @functools.wraps(f)
        def _(*a, **kw):
            if not current_app.config["USE_REDIS"]:
                return f(*a, **kw)
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            key = key + ":" + request.query_string.decode()
            force = kw.pop("force", False)
            r = rdb.get(key) if not force else None
            if r is None:
                r = f(*a, **kw)
                if r is not None:
                    if not isinstance(r, BUILTIN_TYPES):
                        r = dumps(r)
                    rdb.set(key, r, expire)
                else:
                    r = dumps(empty)
                    rdb.set(key, r, expire)

            try:
                r = loads(r)
            except (TypeError, UnpicklingError):
                pass
            if isinstance(r, Empty):
                r = None
            return r

        _.original_function = f
        return _

    return deco
