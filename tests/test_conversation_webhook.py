import unittest
from datetime import datetime
from messagebird import ConversationClient
from messagebird.conversation_webhook import \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED,\
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestConversationWebhook(unittest.TestCase):

    def test_conversation_webhook_create(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"20c308852190485bbb658e43baffc5fa","url":"https://example.com","channelId":"c0dae31e440145e094c4708b7d908842","events":["conversation.created","conversation.updated"],"status":"enabled","createdDatetime":"2019-04-03T07:46:37.984026573Z","updatedDatetime":null}'

        webhookRequestData = {
          'channelId': '20c308852190485bbb658e43baffc5fa',
          'events': [CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED, CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED],
          'url': 'https://example.com'
        }

        ConversationClient('', http_client).create_webhook(webhookRequestData)

        http_client.request.assert_called_once_with('webhooks', 'POST', webhookRequestData)