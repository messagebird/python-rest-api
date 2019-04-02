import unittest
from datetime import datetime
from messagebird import ConversationClient

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestConversationMessage(unittest.TestCase):

    def test_conversation_list_messages(self):
        http_client = Mock()
        http_client.request.return_value = '{"count":1,"items":[{"id":"54445534","conversationId":"54345543543","channelId":"4535434354","type":"text","content":{"text":"Hello"},"direction":"sent","status":"delivered","createdDatetime":"2019-04-02T08:54:54.608157775Z","updatedDatetime":"2019-04-02T08:54:54.63910221Z"}],"limit":10,"offset":0,"totalCount":1}'

        msg = ConversationClient('', http_client).list_messages(54567)

        self.assertEqual(1, msg.count)
        self.assertEqual('54445534', msg.items[0].id)

        http_client.request.assert_called_once_with('conversations/54567/messages', 'GET', None)