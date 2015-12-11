# -*- coding: utf-8 -*-
import collections


CRLF = '\r\n'


class Headers(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        key = self.__keytransform__(key)
        return self._store[key] if key in self._store else ''

    def __setitem__(self, key, val):
        self._store[self.__keytransform__(key)] = str(val).strip()

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __contains__(self, key):
        return self.__keytransform__(key) in self._store

    def __keytransform__(self, key):
        return str(key).strip()

    def __format__(self, key, val):
        return key + ': ' + val + CRLF

    def __repr__(self):
        return str(dict(self._store))

    def dump(self):
        return ''.join(
            self.__format__(key, val) for (key, val) in self._store.items()
            ) + CRLF

    def add(self, headers):
        if (isinstance(headers, dict) or
                isinstance(headers, collections.Mapping)):
            self.update(headers)
        elif isinstance(headers, str):
            lines = headers.splitlines()
            for line in lines:
                pair = line.split(':')
                if len(pair) >= 2:
                    self[pair[0]] = pair[1]

    @staticmethod
    def load(msg):
        headers = Headers()
        headers.add(msg)
        return headers
