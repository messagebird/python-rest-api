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

    def test_purchase_number(self):
        http_client = Mock()
        http_client.request.return_value = '{"number":"31971234567","country":"NL","region":"Haarlem","locality":"Haarlem","features":["sms","voice"],"tags":[],"type":"landline_or_mobile","status":"active","createdAt":"2019-04-25T14:04:04Z","renewalAt":"2019-05-25T00:00:00Z"}'

        number = Client('', http_client).purchase_number('31971234567', 'NL', 1)

        http_client.request.assert_called_once_with(
            'phone-numbers', 'POST',
            {
                "number": "31971234567",
                "countryCode": "NL",
                "billingIntervalMonths": 1
            }
        )

        self.assertEqual('Haarlem', number.region)
        self.assertEqual(["sms", "voice"], number.features)

    def test_delete_number(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).delete_number('31971234567')

        http_client.request.assert_called_once_with('phone-numbers/31971234567', 'DELETE', None)

    def test_delete_number_invalid(self):
        http_client = Mock()
        http_client.request.return_value = '{"errors": [{"code": 20, "description": "number not found", "parameter": null}]}'

        with self.assertRaises(ErrorException):
            Client('', http_client).delete_number('non-existent-number')

        http_client.request.assert_called_once_with('phone-numbers/non-existent-number', 'DELETE', None)

