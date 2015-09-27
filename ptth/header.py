# -*- coding: utf-8 -*-
import collections


CRLF = '\r\n'


def default_headers():
    return Headers({
        'Accept': '*/*',
        'Accept-Encoding': ', '.join(('gzip', 'deflate'))
    })


def load(msg):
    headers = Headers()
    headers.add(msg)
    return headers


class Headers(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._store[self.__keytransform__(key)]

    def __setitem__(self, key, val):
        self._store[self.__keytransform__(key)] = str(val).strip()

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __keytransform__(self, key):
        return str(key).strip()

    def __format__(self, key, val):
        return key + ': ' + val + CRLF

    def dump(self):
        return ''.join(
            self.__format__(key, val) for (key, val) in self._store.items()
            ) + CRLF

    def add(self, msg):
        lines = msg.splitlines()
        for line in lines:
            pair = line.split(':')
            if len(pair) >= 2:
                self[pair[0]] = pair[1]
