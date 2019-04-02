import unittest
from datetime import datetime
from messagebird import ConversationClient

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestConversation(unittest.TestCase):

    def test_conversation_start(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"1234","contactId":"1234","contact":{"id":"1234","href":"https://contacts.messagebird.com/v2/contacts/1234","msisdn":99999999999,"displayName":"99999999999","firstName":"","lastName":"","customDetails":{},"attributes":{},"createdDatetime":"2019-04-02T08:19:37Z","updatedDatetime":"2019-04-02T08:19:38Z"},"channels":[{"id":"1234","name":"channel-name","platformId":"sms","status":"active","createdDatetime":"2019-04-01T15:25:12Z","updatedDatetime":"0001-01-01T00:00:00Z"}],"status":"active","createdDatetime":"2019-04-02T08:19:37Z","updatedDatetime":"2019-04-02T08:54:42.497114599Z","lastReceivedDatetime":"2019-04-02T08:54:42.464955904Z","lastUsedChannelId":"1234","messages":{"totalCount":1,"href":"https://conversations.messagebird.com/v1/conversations/1234/messages"}}'

        data = {
            'channelId':  '1234',
            'to': '+99999999999',
            'type': "text",
            'content': {
                'text': 'Message Example'
            },
        }

        msg = ConversationClient('', http_client).start(data)

        http_client.request.assert_called_once_with('conversations/start', 'POST', data)

        self.assertEqual('1234', msg.id)
        self.assertEqual(99999999999, msg.contact.msisdn)
        self.assertEqual(datetime(2019, 4, 2, 8, 19, 37), msg.contact.createdDatetime)
        self.assertEqual(datetime(2019, 4, 2, 8, 19, 38), msg.contact.updatedDatetime)
        self.assertEqual('channel-name', msg.channels[0].name)