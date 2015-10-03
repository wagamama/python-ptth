# -*- coding: utf-8 -*-
import threading
import socket
from select import select
from urlparse import urlparse
import header
import request
import response


class Handler(object):
    def __init__(self):
        pass

    def ready_to_handle(self):
        pass

    def handle_request(self, request):
        pass

    def handle_error(self, error):
        pass

    def handle_close(self):
        pass


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
        self._headers = header.Headers({
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'Connection': 'Upgrade',
            'Upgrade': 'PTTH/1.0'})
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
            r_list, _, x_list = select([self._socket], [], [self._socket])

            for x in x_list:
                if not self._stop_event.is_set():
                    self_handler.handle_error()

            if self._stop_event.is_set():
                break

            for r_ready in r_list:
                if r_ready == self._socket:
                    data = self._socket.recv(4096)
                    if data is None:
                        self._handler.handle_close()
                    else:
                        self._handler.handle_request(data)
                        self._socket.send(
                            response.Response(200).dump()
                        )

        self._handler.handle_close()

    def stop(self):
        self._stop_event.set()
        self._socket.shutdown(socket.SHUT_RD)
        self._socket.close()
