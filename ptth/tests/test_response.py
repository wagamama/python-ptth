# -*- coding: utf-8 -*-
import unittest
import ptth


class TestResponse(unittest.TestCase):
    def test_dump(self):
        r = ptth.Response(200,
                          headers=ptth.Headers({'a': 'b'}),
                          data='test')
        self.assertEqual('HTTP/1.1 200 OK\r\n' +
                         'a: b\r\n' +
                         '\r\n' +
                         'test',
                         r.dump())

    def test_dump_no_data(self):
        r = ptth.Response(200,
                          headers=ptth.Headers({'a': 'b'}))
        self.assertEqual('HTTP/1.1 200 OK\r\n' +
                         'a: b\r\n' +
                         '\r\n',
                         r.dump())

    def test_dump_no_headers(self):
        r = ptth.Response(200,
                          data='test data')
        self.assertEqual('HTTP/1.1 200 OK\r\n' +
                         '\r\n' +
                         'test data',
                         r.dump())

    def test_dump_default(self):
        r = ptth.Response(400)
        self.assertEqual('HTTP/1.1 400 Bad Request\r\n' +
                         '\r\n',
                         r.dump())

    def test_status(self):
        r = ptth.Response(500)
        self.assertEqual(500, r.status)
        self.assertEqual('Internal Server Error', r.reason)

    def test_headers(self):
        r = ptth.Response(404, headers=ptth.Headers({'a': 'b'}))
        self.assertEqual('b', r.headers['a'])

    def test_data(self):
        r = ptth.Response(404, data='abcdefg\n')
        self.assertEqual('abcdefg\n', r.data)

    def test_load(self):
        r = ptth.Response.load('HTTP/1.1 202 Accepted\r\n' +
                               'header1: value1\r\n' +
                               'header2: value2\r\n' +
                               '\r\n' +
                               'this is response data\n')
        self.assertIsNotNone(r)
        self.assertEqual(202, r.status)
        self.assertEqual('Accepted', r.reason)
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('value2', r.headers['header2'])
        self.assertEqual('this is response data\n', r.data)

    def test_load_no_header_data(self):
        r = ptth.Response.load('HTTP/1.1 202 Accepted\r\n' +
                               '\r\n')
        self.assertIsNotNone(r)
        self.assertEqual(202, r.status)
        self.assertEqual('Accepted', r.reason)

    def test_load_no_data(self):
        r = ptth.Response.load('HTTP/1.1 202 Accepted\r\n' +
                               'header1: value1\r\n' +
                               '\r\n')
        self.assertIsNotNone(r)
        self.assertEqual(202, r.status)
        self.assertEqual('Accepted', r.reason)
        self.assertEqual('value1', r.headers['header1'])

    def test_load_no_header(self):
        r = ptth.Response.load('HTTP/1.1 202 Accepted\r\n' +
                               '\r\n' +
                               'test data')
        self.assertIsNotNone(r)
        self.assertEqual(202, r.status)
        self.assertEqual('Accepted', r.reason)
        self.assertEqual('test data', r.data)

    def test_load_wrong_status(self):
        r = ptth.Response.load('HTTP/1.1 200OK')
        self.assertIsNone(r)
        r = ptth.Response.load('HTTP/1.1 200OK\r\n')
        self.assertIsNone(r)
        r = ptth.Response.load('HTTP/1.1 200OK\r\n' +
                               'header1: value1\r\n' +
                               '\r\n')
        self.assertIsNone(r)

    def test_load_wrong_header(self):
        r = ptth.Response.load('HTTP/1.1 200 OK\r\n' +
                               'header1: value1\r\n')
        self.assertIsNone(r)

    def test_load_data_with_CRLF(self):
        r = ptth.Response.load('HTTP/1.1 200 OK\r\n' +
                               'header1: value1\r\n' +
                               '\r\n' +
                               '\r\n' +
                               'sample data')
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status)
        self.assertEqual('OK', r.reason)
        self.assertEqual('value1', r.headers['header1'])
        self.assertEqual('\r\nsample data', r.data)


if __name__ == '__main__':
    unittest.main()
