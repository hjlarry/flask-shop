class LocalCache:
    def __init__(self, size=10000):
        self.dataset = {}
        self.size = size

    def clear(self):
        self.dataset.clear()

    def _cache(self, key, value):
        if len(self.dataset) >= self.size:
            self.clear()
        self.dataset[key] = value

    def __repr__(self):
        return "<LocalCache>"

    def get(self, key):
        return self.dataset.get(key)

    def get_multi(self, keys):
        return dict((k, self.get(k)) for k in keys)

    def get_list(self, keys):
        return [self.get(k) for k in keys]

    def set(self, key, value, time=0, compress=True):
        self._cache(key, value)
        return True

    def __getattr__(self, name):
        if name in ("add", "replace", "delete", "incr", "decr", "prepend", "append"):

            def func(key, *args, **kwargs):
                self.dataset.pop(key, None)
                return True

            return func
        elif name in ("append_multi", "prepend_multi", "delete_multi"):

            def func2(keys, *args, **kwargs):
                for k in keys:
                    self.dataset.pop(k, None)
                return True

            return func2
        raise AttributeError(name)


lc = LocalCache()
