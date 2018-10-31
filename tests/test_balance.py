import unittest
from messagebird import Client

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestBalance(unittest.TestCase):

    def test_balance(self):
        http_client = Mock()
        http_client.request.return_value = '{"payment": "prepaid","type": "credits","amount": 9.2}'

        balance = Client('', http_client).balance()

        http_client.request.assert_called_once_with('balance', 'GET', None)

        self.assertEqual('prepaid', balance.payment)
        self.assertEqual('credits', balance.type)
