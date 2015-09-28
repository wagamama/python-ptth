# -*- coding: utf-8 -*-
import header
import httplib
import re


CRLF = header.CRLF
STATUS_PATTERN = str(
    '^HTTP/\d\.\d' +
    '\s+' +
    '([0-9]{3})')
STATUS_RE = re.compile(STATUS_PATTERN)


def parse_status(msg):
    status = 0

    match = STATUS_RE.match(msg)
    if match is not None:
        groups = match.groups(0)
        status = int(groups[0])

    return status


def load(msg):
    lines = msg.split(CRLF)
    status = parse_status(lines[0])
    headers = header.Headers()
    for header_str in lines[1:-1]:
        headers.add(header_str)
    data = lines[-1] if len(lines[-1]) > 0 else None

    return Response(status, headers, data)


class Response(object):
    def __init__(self, status, headers=None, data=None):
        self.status = status
        self.headers = headers if headers is not None else header.Headers()
        self.data = data

    def add_header(self, key, value):
        self.headers[key] = value

    def add_data(self, data):
        self.data = data

    def dump(self):
        response_str = 'HTTP/1.1 {} {}{}{}'.format(
            self.status,
            httplib.responses[self.status],
            CRLF,
            self.headers.dump())

        if self.data is not None:
            response_str += self.data

        return response_str
