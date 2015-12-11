# -*- coding: utf-8 -*-
import unittest
import ptth


class TestHeaders(unittest.TestCase):
    def test_str_key_value(self):
        headers = ptth.Headers()
        headers[0] = 0
        headers['a'] = 0
        self.assertTrue('0' in headers)
        self.assertEqual('0', headers['a'])
        self.assertEqual('', headers['noSuchKey'])

    def test_default_key(self):
        headers = ptth.Headers({
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('gzip', 'deflate'))})
        self.assertTrue('Accept' in headers)
        self.assertTrue('Accept-Encoding' in headers)

    def test_default_value(self):
        headers = ptth.Headers({
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('gzip', 'deflate'))})
        self.assertEqual('*/*', headers['Accept'])
        self.assertEqual(', '.join(('gzip', 'deflate')),
                         headers['Accept-Encoding'])

    def test_dump_default(self):
        headers = ptth.Headers({
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('gzip', 'deflate'))})
        self.assertEqual('Accept-Encoding: gzip, deflate\r\n' +
                         'Accept: */*\r\n' +
                         '\r\n',
                         headers.dump())

    def test_add_str(self):
        headers = ptth.Headers()
        headers.add('a: b\r\n' +
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

    def test_add_dict(self):
        headers = ptth.Headers()
        headers.add({
            'a': 'b',
            'c': 'd',
            'e': 'f'})
        self.assertEqual(3, len(headers))
        self.assertTrue('a' in headers)
        self.assertTrue('c' in headers)
        self.assertTrue('e' in headers)
        self.assertEqual('b', headers['a'])
        self.assertEqual('d', headers['c'])
        self.assertEqual('f', headers['e'])

    def test_add_headers(self):
        headers = ptth.Headers({'a': 'z'})
        headers2 = ptth.Headers({
            'a': 'b',
            'c': 'd',
            'e': 'f'})
        headers.add(headers2)
        self.assertEqual(3, len(headers))
        self.assertTrue('a' in headers)
        self.assertTrue('c' in headers)
        self.assertTrue('e' in headers)
        self.assertEqual('b', headers['a'])
        self.assertEqual('d', headers['c'])
        self.assertEqual('f', headers['e'])

    def test_load(self):
        headers = ptth.Headers.load('a: b\r\n' +
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

    def test_load_empty(self):
        headers = ptth.Headers.load('')
        self.assertEqual(0, len(headers))
        self.assertFalse('a' in headers)
        self.assertEqual('', headers['a'])


if __name__ == '__main__':
    unittest.main()
