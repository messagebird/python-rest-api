import unittest

from messagebird import Client
from messagebird.client import VOICE_WEB_HOOKS_PATH, VOICE_API_ROOT

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestVoiceWebhook(unittest.TestCase):

    def test_voice_webhook_read(self):
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
