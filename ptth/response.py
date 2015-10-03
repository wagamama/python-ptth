# -*- coding: utf-8 -*-
import header
import httplib
import re


CRLF = header.CRLF
STATUS_PATTERN = str(
    '^HTTP/\d\.\d' +
    '\s+' +
    '([0-9]{3})' +
    '\s+')
STATUS_RE = re.compile(STATUS_PATTERN)


def parse_status(msg):
    status = None

    match = STATUS_RE.match(msg)
    if match is not None:
        groups = match.groups(0)
        status = int(groups[0])

    return status


class Response(object):
    def __init__(self, status, headers=None, data=None):
        self.status = status
        self.headers = headers if headers is not None else header.Headers()
        self.data = data

    @property
    def reason(self):
        try:
            reason = httplib.responses[self.status]
        except KeyError:
            reason = ''

        return reason

    def add_header(self, key, value):
        self.headers[key] = value

    def add_data(self, data):
        self.data = data

    def dump(self):
        response_str = 'HTTP/1.1 {} {}{}{}'.format(
            self.status,
            self.reason,
            CRLF,
            self.headers.dump())

        if self.data is not None:
            response_str += self.data

        return response_str

    @staticmethod
    def load(msg):
        msg = msg.split(CRLF+CRLF, 1)

        if len(msg) != 2:
            return None

        data = msg[1]
        msg = msg[0].split(CRLF, 1)
        status = parse_status(msg[0])

        if status is None:
            return None

        headers = msg[1] if len(msg) == 2 else ''
        headers = header.Headers.load(headers)
        
        return Response(status, headers, data)
