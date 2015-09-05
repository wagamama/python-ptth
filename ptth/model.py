# -*- coding: utf-8 -*-
import collections


class Headers(collections.MutableMapping):
    @classmethod
    def default_headers(cls):
        return cls({
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('gzip', 'deflate'))
        })

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, val):
        self._store[key] = val

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return ''.join(
            self.__format__(key, val) for (key, val) in self._store.items()
        ) + '\r\n'

    def __format__(self, key, val):
        return str(key) + ': ' + str(val) + '\r\n'
