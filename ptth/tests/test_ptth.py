# -*- coding: utf-8 -*-
import threading
import socket
from select import select
import unittest
import ptth


class TestServer(threading.Thread):
    def __init__(self, ready_event):
        super(TestServer, self).__init__()
        self._ready_event = ready_event
        self._stop_event = threading.Event()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 7000))
        sock.listen(5)
        conn, _ = sock.accept()

        while True:
            r_list, _, _ = select([conn], [], [])

            if self._stop_event.is_set():
                conn.close()
                break

            if len(r_list) > 0:
                data = conn.recv(4096)
                if not data:
                    break
                else:
                    req = ptth.Request.load(data)
                    if (req.method == 'POST' and
                        req.headers['Connection'] == 'Upgrade' and
                        req.headers['Upgrade'] == 'PTTH/1.0'):
                        if self.error:
                            conn.send(ptth.Response(200).dump())
                        else:
                            conn.send(ptth.Response(101).dump())
                            self._ready_event.wait()
                            conn.send(ptth.Request('POST', '/').dump())

        sock.close()

    def serve(self, error=False):
        self.error = error
        self.start()

    def close(self):
        self._stop_event.set()
        

class TestHandler(ptth.Handler):
    def __init__(self, events):
        self.events = events
        self.ready = False
        self.request = False
        self.error = False
        self.close = False

    def ready_to_handle(self):
        self.ready = True
        if self.events['ready'] is not None:
            self.events['ready'].set()

    def handle_request(self, request):
        self.request = True
        if self.events['request'] is not None:
            self.events['request'].set()

    def handle_error(self, error):
        self.error = True
        if self.events['error'] is not None:
            self.events['error'].set()

    def handle_close(self):
        self.close = True
        if self.events['close'] is not None:
            self.events['close'].set()
       

class TestPTTH(unittest.TestCase):
    def setUp(self):
        self.events = {}
        self.events['ready'] = threading.Event()
        self.events['request'] = threading.Event()
        self.events['error'] = threading.Event()
        self.events['close'] = threading.Event()
        self.ready_event = threading.Event()
        self.handler = TestHandler(self.events)
        self.server = TestServer(self.ready_event)

    def tearDown(self):
        self.server.close()

    def test_ptth(self):
        self.server.serve()
        s = ptth.Session(self.handler)
        s.serve('http://localhost:7000/')
        self.events['ready'].wait()
        self.ready_event.set()
        self.events['request'].wait()
        s.close()
        self.events['close'].wait()

        self.assertTrue(self.handler.ready)
        self.assertTrue(self.handler.request)
        self.assertFalse(self.handler.error)
        self.assertTrue(self.handler.close)

    def test_error(self):
        self.server.serve(error=True)
        s = ptth.Session(self.handler)
        s.serve('http://localhost:7000/')
        self.events['error'].wait()
        s.close()
        self.events['close'].wait()

        self.assertFalse(self.handler.ready)
        self.assertFalse(self.handler.request)
        self.assertTrue(self.handler.error)
        self.assertTrue(self.handler.close)


if __name__ == '__main__':
    unittest.main()
