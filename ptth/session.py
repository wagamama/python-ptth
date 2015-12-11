# -*- coding: utf-8 -*-
import threading
import socket
from select import select
from urlparse import urlparse
from .header import Headers
from .request import Request
from .response import Response
from .exception import *


class Handler(object):
    def ready_to_handle(self):
        print 'ready to handle'

    def handle_request(self, request):
        print 'handle request'

    def handle_error(self, error):
        print 'handle error'

    def handle_close(self):
        print 'handle close'


class Session(threading.Thread):
    def __init__(self, handler):
        super(Session, self).__init__()
        self._handler = handler
        self._upgraded = False
        self._stop_event = threading.Event()
        self._socket = None

    def _init_url(self, url):
        result = urlparse(url)

        if result.scheme == 'http':
            self._host = result.hostname
            self._port = result.port if result.port else 80
            self._url = result.path
        else:
            raise PtthUrlError()

    def _ptth_headers(self):
        return Headers({
            'Connection': 'Upgrade',
            'Upgrade': 'PTTH/1.0'})

    def _init_ptth_request(self, url, headers):
        self._init_url(url)
        ptth_headers = self._ptth_headers()
        ptth_headers.add(headers)
        self._ptth_request = Request('POST', self._url, ptth_headers)

    def _check_ptth_response(self, data):
        response = Response.load(data)
        if response.status == 101:
            self._upgraded = True
        else:
            raise PtthUpgradeFailed()

    def serve(self, url, headers=None):
        self._init_ptth_request(url, headers)
        self.start()

    def run(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._socket.send(self._ptth_request.dump())

        while True:
            r_list, _, x_list = select([self._socket], [], [self._socket])

            if len(x_list) > 0:
                if not self._stop_event.is_set():
                    self_handler.handle_error()

            if self._stop_event.is_set():
                self._socket.close()
                break

            if len(r_list) > 0:
                data = self._socket.recv(4096)
                if not data:
                    break
                elif not self._upgraded:
                    try:
                        self._check_ptth_response(data)
                    except PtthError as e:
                        self._handler.handle_error(e)
                    else:
                        self._handler.ready_to_handle()
                else:
                    request = Request.load(data)
                    response = self._handler.handle_request(request)
                    if response is not None:
                        self._socket.send(response.dump())

        self._handler.handle_close()

    def close(self):
        self._stop_event.set()
        if self._socket is not None:
            self._socket.shutdown(socket.SHUT_RD)
