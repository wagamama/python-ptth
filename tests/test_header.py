# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('../')
from ptth import header


class TestHeaders(unittest.TestCase):
    def test_str_key_value(self):
        headers = header.Headers()
        headers[0] = 0
        headers['a'] = 0
        self.assertTrue('0' in headers)
        self.assertEqual('0', headers['a'])

    def test_default_key(self):
        headers = header.default_headers()
        self.assertTrue('Accept' in headers)
        self.assertTrue('Accept-Encoding' in headers)

    def test_default_value(self):
        headers = header.default_headers()
        self.assertEqual('*/*', headers['Accept'])
        self.assertEqual(', '.join(('gzip', 'deflate')),
                         headers['Accept-Encoding'])

    def test_dump_default(self):
        headers = header.default_headers()
        self.assertEqual('Accept-Encoding: gzip, deflate\r\n' +
                         'Accept: */*\r\n' +
                         '\r\n',
                         headers.dump())

    def test_default_add(self):
        headers = header.default_headers()
        headers.add('a: b\r\n' +
                    'c: d\r\n' +
                    'e: f\r\n' +
                    '\r\n')
        self.assertEqual(5, len(headers))
        self.assertTrue('a' in headers)
        self.assertTrue('c' in headers)
        self.assertTrue('e' in headers)
        self.assertEqual('b', headers['a'])
        self.assertEqual('d', headers['c'])
        self.assertEqual('f', headers['e'])

    def test_load(self):
        headers = header.Headers()
        headers.load('a: b\r\n' +
                     'c: d\r\n' +
                     'e: f\r\n' +
                     '\r\n')
        self.assertEqual(3, len(headers))
        self.assertTrue('a' in headers)
        self.assertTrue('c' in headers)
        self.assertTrue('e' in headers)
        self.assertEqual('b', headers['a'])
        self.assertEqual('d', headers['c'])
        self.assertEqual('f', headers['e'])


if __name__ == '__main__':
    unittest.main()
