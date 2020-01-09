import unittest
from messagebird import Client, ErrorException

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestNumber(unittest.TestCase):

    def test_available_numbers_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"items":[{"number":"3197010260188","country":"NL","region":"","locality":"","features":["sms","voice"],"type":"mobile"}],"limit":20,"count":1}'

        numbers = Client('', http_client).available_numbers_list('NL', {'number': 319})

        http_client.request.assert_called_once_with('available-phone-numbers/NL', 'GET', {'number': 319, 'limit': 20, 'offset': 0})

        self.assertEqual(1, numbers.count)
        self.assertEqual(1, len(numbers.items))
        self.assertEqual('3197010260188', numbers.items[0].number)
