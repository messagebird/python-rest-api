import unittest
from messagebird import Client

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestMessage(unittest.TestCase):

    def test_message(self):
        http_client = Mock()
        http_client.request.return_value = '{"body": "Hello World","createdDatetime": "2015-01-05T10:02:59+00:00","datacoding": "plain","direction": "mt","gateway": 239,"href": "https://rest.messagebird.com/messages/message-id","id": "message-id","mclass": 1,"originator": "TestName","recipients": {"items": [{"recipient": 31612345678,"status": "sent","statusDatetime": "2015-01-05T10:02:59+00:00"}],"totalCount": 1,"totalDeliveredCount": 0,"totalDeliveryFailedCount": 0,"totalSentCount": 1},"reference": null,"scheduledDatetime": null,"type": "sms","typeDetails": {},"validity": null}'

        message = Client('', http_client).message('message-id')

        http_client.request.assert_called_once_with('messages/message-id', 'GET', None)

        self.assertEqual('mt', message.direction)

    def test_message_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).message_create('MessageBird', ['31612345678', '31687654321'], 'Hello World', {'datacoding': 'unicode'})

        http_client.request.assert_called_once_with('messages', 'POST', {'datacoding': 'unicode', 'originator': 'MessageBird', 'body': 'Hello World', 'recipients': '31612345678,31687654321' })

    def test_message_delete(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).message_delete('message-id')

        http_client.request.assert_called_once_with('messages/message-id', 'DELETE', None)
