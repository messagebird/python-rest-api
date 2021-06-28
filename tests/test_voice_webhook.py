import unittest
from unittest.mock import Mock

from messagebird import Client
from messagebird.client import VOICE_WEB_HOOKS_PATH, VOICE_API_ROOT
from messagebird.error import ValidationError
from messagebird.serde import json_serialize
from messagebird.voice_webhook import VoiceCreateWebhookRequest, VoiceUpdateWebhookRequest


class TestVoiceWebhook(unittest.TestCase):

    def test_voice_read_webhook(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "534e1848-235f-482d-983d-e3e11a04f58a",
              "url": "https://example.com/",
              "token": "foobar",
              "createdAt": "2017-03-15T13:28:32Z",
              "updatedAt": "2017-03-15T13:28:32Z"
            }
          ],
          "_links": {
            "self": "/webhooks/534e1848-235f-482d-983d-e3e11a04f58a"
          }
        }'''
        webhook_id = '534e1848-235f-482d-983d-e3e11a04f58a'
        webhook_token = 'foobar'

        voice_webhook = Client('', http_client).voice_read_webhook(webhook_id)

        http_client.request.assert_called_once_with(
            VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '/' + webhook_id, 'GET', None)

        self.assertEqual(webhook_id, voice_webhook.id)
        self.assertEqual(webhook_token, voice_webhook.token)

    def test_voice_list_webhook(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "534e1848-235f-482d-983d-e3e11a04f58a",
              "url": "https://example.com/",
              "token": "foobar",
              "createdAt": "2017-03-15T13:28:32Z",
              "updatedAt": "2017-03-15T13:28:32Z",
              "_links": {
                "self": "/webhooks/534e1848-235f-482d-983d-e3e11a04f58a"
              }
            },
            {
              "id": "123e345-235f-482d-983d-e3e11a04f58a",
              "url": "https://gogol.com/",
              "token": "barbar",
              "createdAt": "2017-03-15T13:28:32Z",
              "updatedAt": "2017-03-15T13:28:32Z",
              "_links": {
                "self": "/webhooks/534e1848-235f-482d-983d-e3e11a04f58a"
              }
            }
          ],
          "_links": {
            "self": "/webhooks?page=1"
          },
          "pagination": {
            "totalCount": 1,
            "pageCount": 1,
            "currentPage": 1,
            "perPage": 10
          }
        }'''

        webhook_id = '534e1848-235f-482d-983d-e3e11a04f58a'
        webhook_token = 'foobar'

        voice_webhook_list = Client('', http_client).voice_list_webhooks(limit=10, offset=0)

        http_client.request.assert_called_once_with(
            VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '?limit=10&offset=0', 'GET', None)

        webhooks = voice_webhook_list.data
        self.assertEqual(2, len(webhooks))
        self.assertEqual(webhook_id, webhooks[0].id)
        self.assertEqual(webhook_token, webhooks[0].token)

    def test_voice_create_webhook(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "534e1848-235f-482d-983d-e3e11a04f58a",
              "url": "https://example.com/",
              "token": "foobar",
              "createdAt": "2017-03-15T14:10:07Z",
              "updatedAt": "2017-03-15T14:10:07Z"
            }
          ],
          "_links": {
            "self": "/webhooks/534e1848-235f-482d-983d-e3e11a04f58a"
          }
        }'''

        create_webhook_request = VoiceCreateWebhookRequest(url="https://example.com/", title="FooBar", token="foobar")
        created_webhook = Client('', http_client).voice_create_webhook(create_webhook_request)

        http_client.request.assert_called_once_with(VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH, 'POST',
                                                    create_webhook_request.__dict__())
        self.assertEqual(create_webhook_request.url, created_webhook.url)
        self.assertEqual(create_webhook_request.token, created_webhook.token)

    def test_voice_create_webhook_request_validation(self):
        url = "https://example.com/"
        title = "FooBar"
        token = "FooBarToken"
        blank_string = '    '

        with self.assertRaises(ValidationError):
            VoiceCreateWebhookRequest(title=title)

        request = VoiceCreateWebhookRequest(url=url, title=title)

        self.assertEqual(url, request.url)
        self.assertEqual(title, request.title)
        self.assertEqual(None, request.token)

        request.url = url + url
        with self.assertRaises(ValidationError):
            request.url = blank_string

    def test_voice_update_webhook(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "534e1848-235f-482d-983d-e3e11a04f58a",
              "url": "https://example.com/baz",
              "token": "foobar",
              "createdAt": "2017-03-15T13:27:02Z",
              "updatedAt": "2017-03-15T13:28:01Z"
            }
          ],
          "_links": {
            "self": "/webhooks/534e1848-235f-482d-983d-e3e11a04f58a"
          }
        }'''
        webhook_id = '534e1848-235f-482d-983d-e3e11a04f58a'
        update_webhook_request = VoiceUpdateWebhookRequest(title="FooBar", token="foobar")
        updated_webhook = Client('', http_client).voice_update_webhook(webhook_id, update_webhook_request)

        http_client.request.assert_called_once_with(
            VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '/' + webhook_id, 'PUT', update_webhook_request.__dict__())

        self.assertEqual(update_webhook_request.token, updated_webhook.token)

    def test_voice_delete_webhook(self):
        http_client = Mock()
        http_client.request.return_value = ''
        webhook_id = '534e1848-235f-482d-983d-e3e11a04f58a'
        Client('', http_client).voice_delete_webhook(webhook_id)

        http_client.request.assert_called_once_with(
            VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '/' + webhook_id, 'DELETE', None)

    def test_check_serialization(self):
        json_serialize(VoiceCreateWebhookRequest(url="https://someurl.com", title="foobar"))
        json_serialize(VoiceUpdateWebhookRequest(title="foobar"))
