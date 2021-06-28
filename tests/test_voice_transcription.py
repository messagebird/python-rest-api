import unittest
from unittest.mock import Mock

from messagebird import Client


class TestVoiceTranscription(unittest.TestCase):

    def test_create_voice_transcription(self):
        http_client = Mock()
        http_client.request.return_value = '''
        {
          "data": [
            {
              "id": "fb455b79-c4de-419f-8f72-8c199975c12a",
              "recordingId": "4c444e1e-3cea-4b52-90f7-55dec7b2e05e",
              "status": "done",
              "createdAt": "2019-08-23T13:29:10Z",
              "updatedAt": "2019-08-23T13:29:21Z",
              "legId": "d931d0e8-3385-43b3-964b-c9dda2581213"
            }
          ],
          "_links": {
            "file": "/transcriptions/fb455b79-c4de-419f-8f72-8c199975c12a.txt",
            "self": "/transcriptions/fb455b79-c4de-419f-8f72-8c199975c12a"
          }
        }
        '''

        url = 'https://voice.messagebird.com/calls/'
        call_id = '74bd9fac-742e-4f7c-aef2-bf068c80fd00'
        leg_id = 'd931d0e8-3385-43b3-964b-c9dda2581213'
        recording_id = '4c444e1e-3cea-4b52-90f7-55dec7b2e05e'
        language = 'pt-Br'

        msg = Client('', http_client).voice_transcription_create(
            call_id,
            leg_id,
            recording_id,
            language
        )

        http_client.request.assert_called_once_with(
            url + call_id + '/legs/' + leg_id + '/recordings/' + recording_id + '/transcriptions',
            'POST',
            {'language': language}
        )

        self.assertIsInstance(str(msg), str)

    def test_view_voice_transcription(self):
        http_client = Mock()
        http_client.request.return_value = '''
        {
          "data": [
            {
              "id": "fb455b79-c4de-419f-8f72-8c199975c12a",
              "recordingId": "4c444e1e-3cea-4b52-90f7-55dec7b2e05e",
              "status": "done",
              "createdAt": "2019-08-23T13:29:10Z",
              "updatedAt": "2019-08-23T13:29:21Z",
              "legId": "d931d0e8-3385-43b3-964b-c9dda2581213"
            }
          ],
          "_links": {
            "file": "/transcriptions/fb455b79-c4de-419f-8f72-8c199975c12a.txt",
            "self": "/transcriptions/fb455b79-c4de-419f-8f72-8c199975c12a"
          }
        }
        '''

        url = 'https://voice.messagebird.com/calls/'
        call_id = '74bd9fac-742e-4f7c-aef2-bf068c80fd00'
        leg_id = 'd931d0e8-3385-43b3-964b-c9dda2581213'
        recording_id = '4c444e1e-3cea-4b52-90f7-55dec7b2e05e'
        transcription_id = 'fb455b79-c4de-419f-8f72-8c199975c12a'

        msg = Client('', http_client).voice_transcription_view(
            call_id,
            leg_id,
            recording_id,
            transcription_id
        )

        http_client.request.assert_called_once_with(
            url + call_id + '/legs/' + leg_id + '/recordings/' + recording_id + '/transcriptions/' + transcription_id,
            'GET',
            None
        )

        self.assertIsInstance(str(msg), str)

    def test_list_voice_transcription(self):
        http_client = Mock()
        http_client.request.return_value = '''
        {
          "data": [
            {
              "id": "fb455b79-c4de-419f-8f72-8c199975c12a",
              "recordingId": "4c444e1e-3cea-4b52-90f7-55dec7b2e05e",
              "status": "done",
              "createdAt": "2019-08-23T13:29:10Z",
              "updatedAt": "2019-08-23T13:29:21Z",
              "legId": "d931d0e8-3385-43b3-964b-c9dda2581213"
            }
          ],
          "_links": {
            "file": "/transcriptions/fb455b79-c4de-419f-8f72-8c199975c12a.txt",
            "self": "/transcriptions/fb455b79-c4de-419f-8f72-8c199975c12a"
          }
        }
        '''

        url = 'https://voice.messagebird.com/calls/'
        call_id = '74bd9fac-742e-4f7c-aef2-bf068c80fd00'
        leg_id = 'd931d0e8-3385-43b3-964b-c9dda2581213'
        recording_id = '4c444e1e-3cea-4b52-90f7-55dec7b2e05e'

        msg = Client('', http_client).voice_transcription_list(
            call_id,
            leg_id,
            recording_id
        )

        http_client.request.assert_called_once_with(
            url + call_id + '/legs/' + leg_id + '/recordings/' + recording_id + '/transcriptions',
            'GET',
            None
        )

        self.assertIsInstance(str(msg), str)

    def test_download_voice_transcription(self):
        http_client = Mock()
        http_client.request.return_value = ''

        url = 'https://voice.messagebird.com/calls/'
        call_id = '74bd9fac-742e-4f7c-aef2-bf068c80fd00'
        leg_id = 'd931d0e8-3385-43b3-964b-c9dda2581213'
        recording_id = '4c444e1e-3cea-4b52-90f7-55dec7b2e05e'
        transcription_id = 'fb455b79-c4de-419f-8f72-8c199975c12a'

        Client('', http_client).voice_transcription_download(
            call_id,
            leg_id,
            recording_id,
            transcription_id
        )

        http_client.request.assert_called_once_with(
            url + call_id + '/legs/' + leg_id + '/recordings/' + recording_id + '/transcriptions/' + transcription_id,
            'GET',
            None
        )
