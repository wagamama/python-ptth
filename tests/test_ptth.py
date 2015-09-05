# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
import ptth


if __name__ == '__main__':
    def handler(msg):
        print msg

    s = ptth.Session()
    print str(s._headers)
