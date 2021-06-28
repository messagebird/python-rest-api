import unittest
from unittest.mock import Mock

from messagebird import Client, ErrorException


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

        Client('', http_client).message_create(
            'MessageBird', ['31612345678', '31687654321'], 'Hello World', {'datacoding': 'unicode'})

        http_client.request.assert_called_once_with(
            'messages', 'POST',
            {
                'datacoding': 'unicode',
                'originator': 'MessageBird',
                'body': 'Hello World',
                'recipients': '31612345678,31687654321'
            }
        )

    def test_message_delete(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).message_delete('message-id')

        http_client.request.assert_called_once_with('messages/message-id', 'DELETE', None)

    def test_message_delete_invalid(self):
        http_client = Mock()
        http_client.request.return_value = '{"errors": [{"code": 20, "description": "message not found", "parameter": null}]}'

        with self.assertRaises(ErrorException):
            Client('', http_client).message_delete('non-existent-message-id')

        http_client.request.assert_called_once_with('messages/non-existent-message-id', 'DELETE', None)

    def test_message_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"offset": 0,"limit": 20,"count": 2,"totalCount": 2,"links": {"first": "https://rest.messagebird.com/messages/?offset=0","previous": null,"next": null,"last": "https://rest.messagebird.com/messages/?offset=0"},"items": [{"originator": "TEST","body": "This is a test message, sent through the MessageBird API, using the official Python SDK.","direction": "mt","mclass": 1,"reference": null,"createdDatetime": "2018-07-13T10:34:08+00:00","recipients": {"totalCount": 1,"totalSentCount": 1,"totalDeliveredCount": 1,"totalDeliveryFailedCount": 0,"items": [{"originator": null,"status": "delivered","statusDatetime": "2018-07-13T10:34:13+00:00","recipient": 123456789011}]},"validity": null,"gateway": 1,"typeDetails": {},"href": "https://rest.messagebird.com/messages/first-message-id","datacoding": "plain","scheduledDatetime": null,"type": "sms","id": "first-message-id"},{"originator": "TEST","body": "This is a test message, sent through the MessageBird API, using the official Python SDK.","direction": "mt","mclass": 1,"reference": null,"createdDatetime": "2018-07-13T10:33:52+00:00","recipients": {"totalCount": 1,"totalSentCount": 1,"totalDeliveredCount": 1,"totalDeliveryFailedCount": 0,"items": [{"originator": null,"status": "delivered","statusDatetime": "2018-07-13T10:33:56+00:00","recipient": 123456789012}]},"validity": null,"gateway": 1,"typeDetails": {},"href": "https://rest.messagebird.com/messages/second-message-id","datacoding": "plain","scheduledDatetime": null,"type": "sms","id": "second-message-id"}]}'

        message_list = Client('', http_client).message_list(20, 0)

        http_client.request.assert_called_once_with('messages?limit=20&offset=0', 'GET', None)

        self.assertEqual(2, message_list.totalCount)
        self.assertEqual('https://rest.messagebird.com/messages/?offset=0', message_list.links.first)
        self.assertEqual('https://rest.messagebird.com/messages/first-message-id', message_list.items[0].href)

    def test_scheduled_message_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"offset": 0,"limit": 20,"count": 2,"totalCount": 2,"links": {"first": "https://rest.messagebird.com/messages/?offset=0","previous": null,"next": null,"last": "https://rest.messagebird.com/messages/?offset=0"},"items": []}'

        message_list = Client('', http_client).message_list(20, 0, "scheduled")

        http_client.request.assert_called_once_with('messages?limit=20&offset=0&status=scheduled', 'GET', None)
