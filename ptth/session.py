# -*- coding: utf-8 -*-
import socket
from .model import Headers


class Session(object):
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._headers = Headers.default_headers()

    def request(self):
        pass
