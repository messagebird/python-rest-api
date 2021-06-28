import unittest
from unittest.mock import Mock

from messagebird import Client, ErrorException


class TestVerify(unittest.TestCase):

    def test_verify(self):
        http_client = Mock()
        http_client.request.return_value = '{"id": "verify-id","href": "https://rest.messagebird.com/verify/verify-id","recipient": 31612345678,"reference": "MyReference","messages": {"href": "https://rest.messagebird.com/messages/message-id"},"status": "verified","createdDatetime": "2017-05-30T12:39:50+00:00","validUntilDatetime": "2017-05-30T12:40:20+00:00"}'

        verify = Client('', http_client).verify('verify-id')

        http_client.request.assert_called_once_with('verify/verify-id', 'GET', None)

        self.assertEqual('verify-id', verify.id)

    def test_verify_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).verify_create('31612345678', {})

        http_client.request.assert_called_once_with('verify', 'POST', {'recipient': '31612345678'})

    def test_verify_create_email(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).verify_create_email('recipient@example.com', 'originator@example.com')

        http_client.request.assert_called_once_with('verify', 'POST', {'recipient': 'recipient@example.com', 'originator': 'originator@example.com', 'type': 'email'})

    def test_verify_verify(self):
        http_client = Mock()
        http_client.request.return_value = '{"id": "verify-id","href": "https://rest.messagebird.com/verify/verify-id","recipient": 31612345678,"reference": "MyReference","messages": {"href": "https://rest.messagebird.com/messages/63b168423592d681641eb07b76226648"},"status": "verified","createdDatetime": "2017-05-30T12:39:50+00:00","validUntilDatetime": "2017-05-30T12:40:20+00:00"}'

        verify = Client('', http_client).verify_verify('verify-id', 'secret')

        http_client.request.assert_called_once_with('verify/verify-id', 'GET', {'token': 'secret'})

        self.assertEqual('verified', verify.status)

    def test_verify_delete(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).verify_delete('31612345678')

        http_client.request.assert_called_once_with('verify/31612345678', 'DELETE', None)

    def test_verify_delete_invalid(self):
        http_client = Mock()
        http_client.request.return_value = '{"errors": [{"code": 20,"description": "verification id not found","parameter": null}]}'

        with self.assertRaises(ErrorException):
            Client('', http_client).verify_delete('non-existent-verify-id')

        http_client.request.assert_called_once_with('verify/non-existent-verify-id', 'DELETE', None)
