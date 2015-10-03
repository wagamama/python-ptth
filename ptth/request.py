# -*- coding: utf-8 -*-
import header
import re


CRLF = header.CRLF
METHOD_URL_PATTERN = str(
    '^([A-Z]+)' +
    '\s+' +
    '((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)' +
    '\s+')
METHOD_URL_RE = re.compile(METHOD_URL_PATTERN)


def parse_method_and_url(msg):
    method = None
    url = None

    match = METHOD_URL_RE.match(msg)
    if match is not None:
        groups = match.groups('')
        method = groups[0]
        url = groups[1]

    return (method, url)


class Request(object):
    def __init__(self, method, url, headers=None, data=None):
        self.method = method.upper()
        self.url = url
        self.headers = headers if headers is not None else header.Headers()
        self.data = data

    def add_header(self, key, value):
        self.headers[key] = value

    def add_data(self, data):
        self.data = data

    def dump(self):
        request_str = '{} {} HTTP/1.1{}{}'.format(
            self.method, self.url, CRLF, self.headers.dump())

        if self.data is not None:
            request_str += self.data

        return request_str

    @staticmethod
    def load(msg):
        msg = msg.split(CRLF+CRLF, 1)

        if len(msg) != 2:
            return None

        data = msg[1]
        msg = msg[0].split(CRLF, 1)
        method, url = parse_method_and_url(msg[0])
        
        if method is None or url is None:
            return None

        headers = msg[1] if len(msg) == 2 else ''
        headers = header.Headers.load(headers)

        return Request(method, url, headers, data)
