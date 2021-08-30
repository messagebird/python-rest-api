import time
import unittest

from messagebird.signed_request import SignedRequest

SIGNING_KEY = 'PlLrKaqvZNRR5zAjm42ZT6q1SQxgbbGd'


class TestMessage(unittest.TestCase):

    def test_signed_request_withou_body(self):
        query = {
            'recipient': '31612345678',
            'reference': 'FOO',
            'statusDatetime': '2019-01-11T09:17:11+00:00',
            'id': 'eef0ab57a9e049be946f3821568c2b2e',
            'status': 'delivered',
            'mccmnc': '20408',
            'ported': '1',
        }

        signature = 'KVBdcVdz2lYMwcBLZCRITgxUfA/WkwSi+T3Wxl2HL6w='
        timestamp = 1547198231
        body = ''

        signed_request = SignedRequest(signature, timestamp, body, query)
        self.assertTrue(signed_request.verify(SIGNING_KEY))

    def test_signed_request_with_body(self):
        query = {
            'recipient': '31612345678',
            'reference': 'FOO',
            'statusDatetime': '2019-01-11T09:17:11+00:00',
            'id': 'eef0ab57a9e049be946f3821568c2b2e',
            'status': 'delivered',
            'mccmnc': '20408',
            'ported': '1',
        }

        signature = '2bl+38H4oHVg03pC3bk2LvCB0IHFgfC4cL5HPQ0LdmI='
        timestamp = 1547198231
        body = '{"foo":"bar"}'

        signed_request = SignedRequest(signature, timestamp, body, query)
        self.assertTrue(signed_request.verify(SIGNING_KEY))

    def test_incorrectly_signed_request(self):
        query = {
            'recipient': '31612345678',
            'reference': 'BAR',
            'statusDatetime': '2019-01-11T09:17:11+00:00',
            'id': 'eef0ab57a9e049be946f3821568c2b2e',
            'status': 'delivered',
            'mccmnc': '20408',
            'ported': '1',
        }

        signature = 'KVBdcVdz2lYMwcBLZCRITgxUfA/WkwSi+T3Wxl2HL6w='
        timestamp = 1547198231
        body = ''

        signed_request = SignedRequest(signature, timestamp, body, query)
        self.assertFalse(signed_request.verify(SIGNING_KEY))

    def test_recent_signed_request(self):
        query = {}
        signature = 'KVBdcVdz2lYMwcBLZCRITgxUfA/WkwSi+T3Wxl2HL6w='
        timestamp = int(time.time()) - 1
        body = ''

        signed_request = SignedRequest(signature, timestamp, body, query)
        self.assertTrue(signed_request.is_recent())

    def test_not_recent_signed_request(self):
        query = {}
        signature = 'KVBdcVdz2lYMwcBLZCRITgxUfA/WkwSi+T3Wxl2HL6w='
        timestamp = int(time.time()) - 100
        body = ''

        signed_request = SignedRequest(signature, timestamp, body, query)
        self.assertFalse(signed_request.is_recent())
