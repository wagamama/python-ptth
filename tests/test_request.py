# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('../')
from ptth import request, header


class TestRequest(unittest.TestCase):
    def test_dump_headers(self):
        r = request.Request('GET', '/', header.default_headers())
        self.assertEqual('GET / HTTP/1.1\r\n' +
                         'Accept-Encoding: gzip, deflate\r\n' +
                         'Accept: */*\r\n' +
                         '\r\n',
                         r.dump())

    def test_dump_no_headers(self):
        r = request.Request('POST', '/')
        self.assertEqual('POST / HTTP/1.1\r\n' +
                         '\r\n',
                         r.dump())

    def test_dump_data(self):
        r = request.Request('GET', '/', None, 'test data')
        self.assertEqual('GET / HTTP/1.1\r\n' +
                         '\r\n' +
                         'test data',
                         r.dump())

    def test_add_header(self):
        r = request.Request('POST', '/')
        r.add_header('header1', 'value1')
        r.add_header('header2', 'value2')
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('value2', r.headers['header2'])


    def test_load(self):
        r = request.load('POST /test HTTP/1.1\r\n' +
                         'header1: value1\r\n' +
                         'header2: value2\r\n' +
                         '\r\n' +
                         'this is request data\n')
        self.assertIsNotNone(r)
        self.assertEqual('POST', r.method)
        self.assertEqual('/test', r.url)
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('value2', r.headers['header2'])
        self.assertEqual('this is request data\n', r.data)


if __name__ == '__main__':
    unittest.main()
