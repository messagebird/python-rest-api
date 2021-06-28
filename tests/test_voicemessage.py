import unittest
from unittest.mock import Mock

from messagebird import Client


class TestVoicemessage(unittest.TestCase):

    def test_voicemessage(self):
        http_client = Mock()
        http_client.request.return_value = '{"body": "Hello World","createdDatetime": "2015-01-05T16:11:24+00:00","href": "https://rest.messagebird.com/voicemessages/voicemessage-id","id": "voicemessage-id","ifMachine": "continue","language": "en-gb","originator": "MessageBird","recipients": {"items": [{"recipient": 31612345678,"status": "calling","statusDatetime": "2015-01-05T16:11:24+00:00"}],"totalCount": 1,"totalDeliveredCount": 0,"totalDeliveryFailedCount": 0,"totalSentCount": 1},"reference": null,"repeat": 1,"scheduledDatetime": null,"voice": "female"}'

        voice_message = Client(
            '', http_client).voice_message('voicemessage-id')

        http_client.request.assert_called_once_with(
            'voicemessages/voicemessage-id', 'GET', None)

        self.assertEqual('voicemessage-id', voice_message.id)

    def test_voicemessages_list(self):
        http_client = Mock()
        http_client.request.return_value = '{ "offset": 0, "limit": 10, "count": 2, "totalCount": 2, "links": { "first": "https://rest.messagebird.com/voicemessages/?offset=0&limit=30", "previous": null, "next": null, "last": "https://rest.messagebird.com/voicemessages/?offset=0&limit=30" }, "items": [ { "id": "12345678-9012-3456-7890-123456789012", "href": "https://rest.messagebird.com/voicemessages/12345678-9012-3456-7890-123456789012", "originator": null, "body": "This is a test message.", "reference": null, "language": "en-gb", "voice": "male", "repeat": 1, "ifMachine": "continue", "machineTimeout": 7000, "scheduledDatetime": null, "createdDatetime": "2020-02-04T15:15:30+00:00", "recipients": { "totalCount": 1, "totalSentCount": 1, "totalDeliveredCount": 1, "totalDeliveryFailedCount": 0, "items": [ { "recipient": 31612345678, "originator": null, "status": "answered", "statusDatetime": "2020-02-04T15:15:57+00:00" } ] } }, { "id": "12345678-9012-3456-7890-123456789013", "href": "https://rest.messagebird.com/voicemessages/12345678-9012-3456-7890-123456789013", "originator": null, "body": "The voice message to be sent", "reference": null, "language": "en-gb", "voice": "female", "repeat": 1, "ifMachine": "delay", "machineTimeout": 7000, "scheduledDatetime": null, "createdDatetime": "2020-02-04T12:26:44+00:00", "recipients": { "totalCount": 1, "totalSentCount": 1, "totalDeliveredCount": 1, "totalDeliveryFailedCount": 0, "items": [ { "recipient": 31612345678, "originator": null, "status": "answered", "statusDatetime": "2020-02-04T12:27:32+00:00" } ] } } ] }'

        voice_messages = Client('', http_client).voice_message_list()

        http_client.request.assert_called_once_with(
            'voicemessages?limit=10&offset=0', 'GET', None)

        voice_messages_check = {
            '12345678-9012-3456-7890-123456789012': {
                "id": '12345678-9012-3456-7890-123456789012',
                "href": "https://rest.messagebird.com/voicemessages/12345678-9012-3456-7890-123456789012"
            },
            '12345678-9012-3456-7890-123456789013': {
                "id": '12345678-9012-3456-7890-123456789013',
                "href": "https://rest.messagebird.com/voicemessages/12345678-9012-3456-7890-123456789013"
            }
        }

        for item in voice_messages.items:
            message_specific = voice_messages_check.get(item.id)
            self.assertEqual(message_specific['id'], item.id)
            self.assertEqual(message_specific['href'], item.href)
        self.assertIsInstance(str(voice_messages), str)

    def test_voicemessage_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).voice_message_create(
            ['31612345678', '31687654321'],
            'Hello World',
            {'reference': 'MyReference'}
        )

        http_client.request.assert_called_once_with(
            'voicemessages', 'POST',
            {'body': 'Hello World', 'recipients': '31612345678,31687654321',
             'reference': 'MyReference'}
        )
