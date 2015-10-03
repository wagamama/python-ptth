# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('../')
import ptth


class TestRequest(unittest.TestCase):
    def test_dump(self):
        r = ptth.Request('POST', '/',
                         headers=ptth.Headers({'a': 'b'}),
                         data='test')
        self.assertEqual('POST / HTTP/1.1\r\n' +
                         'a: b\r\n' +
                         '\r\n' +
                         'test',
                         r.dump())

    def test_dump_no_data(self):
        r = ptth.Request('GET', '/',
                         headers=ptth.Headers({'a': 'b'}))
        self.assertEqual('GET / HTTP/1.1\r\n' +
                         'a: b\r\n' +
                         '\r\n',
                         r.dump())

    def test_dump_no_headers(self):
        r = ptth.Request('GET', '/',
                         data='test data')
        self.assertEqual('GET / HTTP/1.1\r\n' +
                         '\r\n' +
                         'test data',
                         r.dump())

    def test_dump_default(self):
        r = ptth.Request('POST', '/')
        self.assertEqual('POST / HTTP/1.1\r\n' +
                         '\r\n',
                         r.dump())

    def test_method_url(self):
        r = ptth.Request('PUT', '/sample')
        self.assertEqual('PUT', r.method)
        self.assertEqual('/sample', r.url)

    def test_add_header(self):
        r = ptth.Request('POST', '/')
        r.add_header('header1', 'value1')
        r.add_header('header2', 'value2')
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('value2', r.headers['header2'])

    def test_add_header_reset(self):
        r = ptth.Request('POST', '/')
        r.add_header('header1', 'value1')
        r.add_header('header1', 'value2')
        self.assertEqual('value2', r.headers['header1'])

    def test_add_data(self):
        r = ptth.Request('PUT', '/')
        r.add_data('abcdefg\n')
        self.assertEqual('abcdefg\n', r.data)

    def test_add_data_reset(self):
        r = ptth.Request('PUT', '/')
        r.add_data('abcdefg\n')
        r.add_data('\ngfedcba')
        self.assertEqual('\ngfedcba', r.data)

    def test_load(self):
        r = ptth.Request.load('POST /test HTTP/1.1\r\n' +
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

    def test_load_no_header_data(self):
        r = ptth.Request.load('POST /test HTTP/1.1\r\n' +
                              '\r\n')
        self.assertIsNotNone(r)
        self.assertEqual('POST', r.method)
        self.assertEqual('/test', r.url)

    def test_load_no_data(self):
        r = ptth.Request.load('POST /test HTTP/1.1\r\n' +
                              'header1: value1\r\n' +
                              '\r\n')
        self.assertIsNotNone(r)
        self.assertEqual('POST', r.method)
        self.assertEqual('/test', r.url)
        self.assertEqual('value1', r.headers['header1'])

    def test_load_no_header(self):
        r = ptth.Request.load('POST /test HTTP/1.1\r\n' +
                              '\r\n' +
                              'this is request data\n')
        self.assertIsNotNone(r)
        self.assertEqual('POST', r.method)
        self.assertEqual('/test', r.url)
        self.assertEqual('this is request data\n', r.data)

    def test_load_wrong_method_url(self):
        r = ptth.Request.load('GET/sample HTTP/1.1')
        self.assertIsNone(r)
        r = ptth.Request.load('GET/sample HTTP/1.1\r\n')
        self.assertIsNone(r)
        r = ptth.Request.load('GET/sample HTTP/1.1\r\n' +
                              'header1: value1\r\n' +
                              '\r\n')
        self.assertIsNone(r)

    def test_load_wrong_header(self):
        r = ptth.Request.load('POST /test HTTP/1.1\r\n' +
                              'header1: value1\r\n')
        self.assertIsNone(r)

    def test_load_data_with_CRLF(self):
        r = ptth.Request.load('GET /sample HTTP/1.1\r\n' +
                              'header1: value1\r\n' +
                              '\r\n' +
                              '\r\n' +
                              'this is data')
        self.assertIsNotNone(r)
        self.assertEqual('GET', r.method)
        self.assertEqual('/sample', r.url)
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('\r\nthis is data', r.data)


if __name__ == '__main__':
    unittest.main()
