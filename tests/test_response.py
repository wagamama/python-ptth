# -*- coding: utf-8 -*-
import unittest
import sys
import httplib

sys.path.append('../')
from ptth import response, header


class TestResponse(unittest.TestCase):
    def test_dump_headers(self):
        r = response.Response(httplib.OK, header.default_headers())
        self.assertEqual('HTTP/1.1 200 OK\r\n' +
                         'Accept-Encoding: gzip, deflate\r\n' +
                         'Accept: */*\r\n' +
                         '\r\n',
                         r.dump())

    def test_dump_no_headers(self):
        r = response.Response(httplib.BAD_REQUEST)
        self.assertEqual('HTTP/1.1 400 Bad Request\r\n' +
                         '\r\n',
                         r.dump())

    def test_dump_data(self):
        r = response.Response(httplib.OK, None, 'test data')
        self.assertEqual('HTTP/1.1 200 OK\r\n' +
                         '\r\n' +
                         'test data',
                         r.dump())

    def test_add_header(self):
        r = response.Response(httplib.NOT_FOUND)
        r.add_header('header1', 'value1')
        r.add_header('header2', 'value2')
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('value2', r.headers['header2'])

    def test_load(self):
        r = response.load('HTTP/1.1 202 Accepted\r\n' +
                          'header1: value1\r\n' +
                          'header2: value2\r\n' +
                          '\r\n' +
                          'this is response data\n')
        self.assertIsNotNone(r)
        self.assertEqual(202, r.status)
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('value2', r.headers['header2'])
        self.assertEqual('this is response data\n', r.data)


if __name__ == '__main__':
    unittest.main()
