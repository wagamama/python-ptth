# -*- coding: utf-8 -*-
import collections


class Headers(collections.MutableMapping):
    SEPARATOR = '\r\n'
    DEFINE = ': '

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
        return self._store[self.__keytransform__(key)]

    def __setitem__(self, key, val):
        self._store[self.__keytransform__(key)] = str(val)

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __keytransform__(self, key):
        return str(key)

    def __format__(self, key, val):
        return key + self.DEFINE + val + self.SEPARATOR

    def dump(self):
        return ''.join(
            self.__format__(key, val) for (key, val) in self._store.items()
            ) + self.SEPARATOR

    def add(self, msg):
        lines = msg.splitlines()
        for line in lines:
            pair = line.split(self.DEFINE)
            if len(pair) >= 2:
                self._store[pair[0]] = pair[1]

    def load(self, msg):
        self._store.clear()
        self.add(msg)
