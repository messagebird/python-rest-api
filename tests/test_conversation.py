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

    def test_conversation_list(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        ConversationClient('', http_client).list()

        http_client.request.assert_called_once_with('conversations', 'GET', None)

    def test_conversation_read(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"57b96dbe0fda40f0a814f5e3268c30a9","contactId":"8846d44229094c20813cf9eea596e680","contact":{"id":"8846d44229094c20813cf9eea596e680","href":"https://contacts.messagebird.com/v2/contacts/8846d44229094c20813cf9eea596e680","msisdn":31617110163,"displayName":"31617110163","firstName":"","lastName":"","customDetails":{},"attributes":{},"createdDatetime":"2019-04-02T08:54:39Z","updatedDatetime":"2019-04-02T08:54:40Z"},"channels":[{"id":"c0dae31e440145e094c4708b7d908842","name":"test","platformId":"sms","status":"active","createdDatetime":"2019-04-01T15:25:12Z","updatedDatetime":"0001-01-01T00:00:00Z"}],"status":"active","createdDatetime":"2019-04-02T08:54:38Z","updatedDatetime":"2019-04-02T14:24:09.192202886Z","lastReceivedDatetime":"2019-04-02T14:24:09.14826339Z","lastUsedChannelId":"c0dae31e440145e094c4708b7d908842","messages":{"totalCount":2,"href":"https://conversations.messagebird.com/v1/conversations/57b96dbe0fda40f0a814f5e3268c30a9/messages"}}'

        conversation = ConversationClient('', http_client).read('conversation-id')

        http_client.request.assert_called_once_with('conversations/conversation-id', 'GET', None)

        self.assertEqual('57b96dbe0fda40f0a814f5e3268c30a9', conversation.id)
        self.assertEqual(datetime(2019, 4, 2, 8, 54, 38), conversation.createdDatetime)
        self.assertEqual(datetime(2019, 4, 2, 14, 24, 9), conversation.updatedDatetime)
        self.assertEqual(datetime(2019, 4, 2, 14, 24), conversation.lastReceivedDatetime)
        self.assertEqual('8846d44229094c20813cf9eea596e680', conversation.contact.id)
        self.assertEqual('c0dae31e440145e094c4708b7d908842', conversation.channels[0].id)
        self.assertEqual(2, conversation.messages.totalCount)