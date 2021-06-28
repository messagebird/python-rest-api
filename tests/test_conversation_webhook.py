import json
import unittest
from datetime import datetime
from unittest.mock import Mock

from dateutil.tz import tzutc

from messagebird import Client
from messagebird.conversation_webhook import \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED, \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED


class TestConversationWebhook(unittest.TestCase):

    def test_conversation_webhook_create(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"20c308852190485bbb658e43baffc5fa","url":"https://example.com","channelId":"c0dae31e440145e094c4708b7d908842","events":["conversation.created","conversation.updated"],"status":"enabled","createdDatetime":"2019-04-03T07:46:37.984026573Z","updatedDatetime":null}'

        webhookRequestData = {
            'channelId': '20c308852190485bbb658e43baffc5fa',
            'events': [CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED,
                       CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED],
            'url': 'https://example.com'
        }

        Client('', http_client).conversation_create_webhook(webhookRequestData)

        http_client.request.assert_called_once_with('webhooks', 'POST', webhookRequestData)

    def test_conversation_webhook_delete(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).conversation_delete_webhook('webhook-id')

        http_client.request.assert_called_once_with('webhooks/webhook-id', 'DELETE', None)

    def test_conversation_webhook_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"offset":0,"limit":10,"count":2,"totalCount":2,"items":[{"id":"57b96dbe0fda40f0a814f5e3268c30a9","contactId":"8846d44229094c20813cf9eea596e680","contact":{"id":"8846d44229094c20813cf9eea596e680","href":"https://contacts.messagebird.com/v2/contacts/8846d44229094c20813cf9eea596e680","msisdn":31617110163,"displayName":"31617110163","firstName":"","lastName":"","customDetails":{},"attributes":{},"createdDatetime":"2019-04-02T08:54:39Z","updatedDatetime":"2019-04-02T08:54:40Z"},"channels":[{"id":"c0dae31e440145e094c4708b7d908842","name":"test","platformId":"sms","status":"active","createdDatetime":"2019-04-01T15:25:12Z","updatedDatetime":"0001-01-01T00:00:00Z"}],"status":"active","createdDatetime":"2019-04-02T08:54:38Z","updatedDatetime":"2019-04-02T14:24:09.192202886Z","lastReceivedDatetime":"2019-04-02T14:24:09.14826339Z","lastUsedChannelId":"c0dae31e440145e094c4708b7d908842","messages":{"totalCount":2,"href":"https://conversations.messagebird.com/v1/conversations/57b96dbe0fda40f0a814f5e3268c30a9/messages"}},{"id":"07e823fdb36a462fb5e187d6d7b96493","contactId":"459a35432b0c4195abbdae353eb19359","contact":{"id":"459a35432b0c4195abbdae353eb19359","href":"https://contacts.messagebird.com/v2/contacts/459a35432b0c4195abbdae353eb19359","msisdn":31615164888,"displayName":"31615164888","firstName":"","lastName":"","customDetails":{},"attributes":{},"createdDatetime":"2019-04-02T08:19:37Z","updatedDatetime":"2019-04-02T08:19:38Z"},"channels":[{"id":"c0dae31e440145e094c4708b7d908842","name":"test","platformId":"sms","status":"active","createdDatetime":"2019-04-01T15:25:12Z","updatedDatetime":"0001-01-01T00:00:00Z"}],"status":"active","createdDatetime":"2019-04-02T08:19:37Z","updatedDatetime":"2019-04-03T07:35:47.35395356Z","lastReceivedDatetime":"2019-04-02T12:02:22.707634424Z","lastUsedChannelId":"c0dae31e440145e094c4708b7d908842","messages":{"totalCount":16,"href":"https://conversations.messagebird.com/v1/conversations/07e823fdb36a462fb5e187d6d7b96493/messages"}}]}'

        Client('', http_client).conversation_list_webhooks()
        http_client.request.assert_called_once_with('webhooks?limit=10&offset=0', 'GET', None)

    def test_conversation_webhook_list_pagination(self):
        http_client = Mock()
        http_client.request.return_value = '{"offset":0,"limit":10,"count":2,"totalCount":2,"items":[{"id":"57b96dbe0fda40f0a814f5e3268c30a9","contactId":"8846d44229094c20813cf9eea596e680","contact":{"id":"8846d44229094c20813cf9eea596e680","href":"https://contacts.messagebird.com/v2/contacts/8846d44229094c20813cf9eea596e680","msisdn":31617110163,"displayName":"31617110163","firstName":"","lastName":"","customDetails":{},"attributes":{},"createdDatetime":"2019-04-02T08:54:39Z","updatedDatetime":"2019-04-02T08:54:40Z"},"channels":[{"id":"c0dae31e440145e094c4708b7d908842","name":"test","platformId":"sms","status":"active","createdDatetime":"2019-04-01T15:25:12Z","updatedDatetime":"0001-01-01T00:00:00Z"}],"status":"active","createdDatetime":"2019-04-02T08:54:38Z","updatedDatetime":"2019-04-02T14:24:09.192202886Z","lastReceivedDatetime":"2019-04-02T14:24:09.14826339Z","lastUsedChannelId":"c0dae31e440145e094c4708b7d908842","messages":{"totalCount":2,"href":"https://conversations.messagebird.com/v1/conversations/57b96dbe0fda40f0a814f5e3268c30a9/messages"}},{"id":"07e823fdb36a462fb5e187d6d7b96493","contactId":"459a35432b0c4195abbdae353eb19359","contact":{"id":"459a35432b0c4195abbdae353eb19359","href":"https://contacts.messagebird.com/v2/contacts/459a35432b0c4195abbdae353eb19359","msisdn":31615164888,"displayName":"31615164888","firstName":"","lastName":"","customDetails":{},"attributes":{},"createdDatetime":"2019-04-02T08:19:37Z","updatedDatetime":"2019-04-02T08:19:38Z"},"channels":[{"id":"c0dae31e440145e094c4708b7d908842","name":"test","platformId":"sms","status":"active","createdDatetime":"2019-04-01T15:25:12Z","updatedDatetime":"0001-01-01T00:00:00Z"}],"status":"active","createdDatetime":"2019-04-02T08:19:37Z","updatedDatetime":"2019-04-03T07:35:47.35395356Z","lastReceivedDatetime":"2019-04-02T12:02:22.707634424Z","lastUsedChannelId":"c0dae31e440145e094c4708b7d908842","messages":{"totalCount":16,"href":"https://conversations.messagebird.com/v1/conversations/07e823fdb36a462fb5e187d6d7b96493/messages"}}]}'

        Client('', http_client).conversation_list_webhooks(2, 1)
        http_client.request.assert_called_once_with('webhooks?limit=2&offset=1', 'GET', None)

    def test_conversation_webhook_read(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"5031e2da142d401c93fbc38518ebb604","url":"https://example.com","channelId":"c0dae31e440145e094c4708b7d908842","events":["conversation.created","conversation.updated"],"status":"enabled","createdDatetime":"2019-04-03T08:41:37Z","updatedDatetime":null}'

        web_hook = Client('', http_client).conversation_read_webhook('webhook-id')

        http_client.request.assert_called_once_with('webhooks/webhook-id', 'GET', None)
        self.assertEqual(datetime(2019, 4, 3, 8, 41, 37, tzinfo=tzutc()), web_hook.createdDatetime)
        self.assertEqual(None, web_hook.updatedDatetime)
        self.assertEqual(['conversation.created', 'conversation.updated'], web_hook.events)

    def test_conversation_webhook_update(self):
        http_client = Mock()
        http_client.request.return_value = json.dumps({"id": "985ae50937a94c64b392531ea87a0263",
                                                       "url": "https://example.com/webhook",
                                                       "channelId": "853eeb5348e541a595da93b48c61a1ae",
                                                       "events": [
                                                           "message.created",
                                                           "message.updated",
                                                       ],
                                                       "status": "enabled",
                                                       "createdDatetime": "2018-08-29T10:04:23Z",
                                                       "updatedDatetime": "2018-08-29T10:10:23Z"
                                                       })

        webhookRequestData = {
            'events': [CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED,
                       CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED],
            'url': 'https://example.com/webhook',
            'status': 'enabled'
        }
        web_hook = Client('', http_client).conversation_update_webhook('webhook-id', webhookRequestData)
        http_client.request.assert_called_once_with('webhooks/webhook-id', 'PATCH', webhookRequestData)
