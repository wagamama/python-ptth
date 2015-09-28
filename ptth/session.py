# -*- coding: utf-8 -*-
import threading
import socket
from select import select
from urlparse import urlparse
import httplib
import header
import request
import response


class Session(threading.Thread):
    def __init__(self, handler):
        super(Session, self).__init__()
        self._handler = handler
        self._stop_event = threading.Event()

    def _parse_url(self, url):
        result = urlparse(url)

        if result.scheme == 'http':
            self._host = result.hostname
            self._port = result.port if result.port else 80
            self._url = result.path
        else:
            pass

    def _construct_headers(self, headers):
        self._headers = header.default_headers()
        self._headers.update({'Connection': 'Upgrade',
                              'Upgrade': 'PTTH/1.0'})

        if not headers:
            return
        elif isinstance(headers, dict):
            self._headers.update(headers)
        elif isinstance(headers, str):
            self._headers.add(headers)

    def serve(self, url, headers=None):
        self._parse_url(url)
        self._construct_headers(headers)
        self.start()

    def run(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._socket.send(
            request.Request('POST', self._url, self._headers).dump())

        while True:
            r_ready_list, _, _ = select([self._socket], [], [])

            if self._stop_event.is_set():
                break

            for r_ready in r_ready_list:
                if r_ready == self._socket:
                    data = self._socket.recv(4096)
                    self._handler.handle_request(data)
                    self._socket.send(
                        response.Response(httplib.OK).dump()
                    )

    def stop(self):
        self._stop_event.set()
        self._socket.shutdown(socket.SHUT_RD)
        self._socket.close()
