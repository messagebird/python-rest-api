import unittest
from messagebird import Client

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestVoicemessage(unittest.TestCase):

    def test_voicemessage(self):
        http_client = Mock()
        http_client.request.return_value = '{"body": "Hello World","createdDatetime": "2015-01-05T16:11:24+00:00","href": "https://rest.messagebird.com/voicemessages/voicemessage-id","id": "voicemessage-id","ifMachine": "continue","language": "en-gb","originator": "MessageBird","recipients": {"items": [{"recipient": 31612345678,"status": "calling","statusDatetime": "2015-01-05T16:11:24+00:00"}],"totalCount": 1,"totalDeliveredCount": 0,"totalDeliveryFailedCount": 0,"totalSentCount": 1},"reference": null,"repeat": 1,"scheduledDatetime": null,"voice": "female"}'

        voice_message = Client('', http_client).voice_message('voicemessage-id')

        http_client.request.assert_called_once_with('voicemessages/voicemessage-id', 'GET', None)

        self.assertEqual('voicemessage-id', voice_message.id)

    def test_voicemessage_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).voice_message_create(['31612345678', '31687654321'], 'Hello World', { 'reference': 'MyReference' })

        http_client.request.assert_called_once_with('voicemessages', 'POST', {'body': 'Hello World', 'recipients': '31612345678,31687654321', 'reference': 'MyReference'})
