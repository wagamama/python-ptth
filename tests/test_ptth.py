# -*- coding: utf-8 -*-
import sys
import time

sys.path.append('../')
import ptth


if __name__ == '__main__':
    class handler:
        def handle_request(self, request):
            print request

        def handle_error(self, error):
            pass

        def handle_close(self):
            pass

    h = handler()
    s = ptth.Session(h)
    s.serve('http://Living-Room-Apple-TV.local:7000/reverse',
            {'User-Agent': 'MediaControl/1.0'})
    time.sleep(5)
    s.stop()
