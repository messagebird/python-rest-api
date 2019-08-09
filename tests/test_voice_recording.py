import unittest
from messagebird import Client
from datetime import datetime

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestVoiceRecording(unittest.TestCase):

    def test_voice_recording_view(self):
        http_client = Mock()
        http_client.request.return_value = '{"data":[{"id":"12345678-9012-3456-7890-123456789012","format":"wav","legId":"87654321-0987-6543-2109-876543210987","status":"done","duration":32,"type":"transfer","createdAt":"2018-01-01T00:00:01Z","updatedAt":"2018-01-01T00:00:05Z","deletedAt":null}],"_links":{"file":"/calls/12348765-4321-0987-6543-210987654321/legs/87654321-0987-6543-2109-876543210987/recordings/12345678-9012-3456-7890-123456789012.wav","self":"/calls/12345678-9012-3456-7890-123456789012/legs/12348765-4321-0987-6543-210987654321/recordings/12345678-9012-3456-7890-123456789012"},"pagination":{"totalCount":0,"pageCount":0,"currentPage":0,"perPage":0}}'

        voice_recording = Client('', http_client).voice_recording_view('12348765-4321-0987-6543-210987654321', '87654321-0987-6543-2109-876543210987', '12345678-9012-3456-7890-123456789012')

        http_client.request.assert_called_once_with('https://voice.messagebird.com/calls/12348765-4321-0987-6543-210987654321/legs/87654321-0987-6543-2109-876543210987/recordings/12345678-9012-3456-7890-123456789012', 'GET', None)

        self.assertEqual('12345678-9012-3456-7890-123456789012', voice_recording.id)
        self.assertEqual('done', voice_recording.status)
        self.assertEqual('wav', voice_recording.format)
        self.assertEqual(datetime(2018, 1, 1, 0, 0, 1), voice_recording.createdAt)
        self.assertEqual(datetime(2018, 1, 1, 0, 0, 5), voice_recording.updatedAt)
        self.assertEqual(2, len(voice_recording._links))

    def test_voice_recording_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"data":[{"id":"12345678-9012-3456-7890-123456789012","format":"wav","legId":"87654321-0987-6543-2109-876543210987","status":"done","duration":32,"type":"transfer","createdAt":"2018-01-01T00:00:01Z","updatedAt":"2018-01-01T00:00:05Z","deletedAt":null,"_links":{"file":"/calls/12348765-4321-0987-6543-210987654321/legs/7654321-0987-6543-2109-876543210987/recordings/12345678-9012-3456-7890-123456789012.wav","self":"/calls/12348765-4321-0987-6543-210987654321/legs/7654321-0987-6543-2109-876543210987/recordings/12345678-9012-3456-7890-123456789012"}},{"id":"12345678-9012-3456-7890-123456789013","format":"wav","legId":"87654321-0987-6543-2109-876543210987","status":"done","duration":12,"type":"transfer","createdAt":"2019-01-01T00:00:01Z","updatedAt":"2019-01-01T00:00:05Z","deletedAt":null,"_links":{"file":"/calls/12348765-4321-0987-6543-210987654321/legs/7654321-0987-6543-2109-876543210987/recordings/12345678-9012-3456-7890-123456789013.wav","self":"/calls/12348765-4321-0987-6543-210987654321/legs/7654321-0987-6543-2109-876543210987/recordings/12345678-9012-3456-7890-123456789013"}}],"_links":{"self":"/calls/12348765-4321-0987-6543-210987654321/legs/7654321-0987-6543-2109-876543210987/recordings?page=1"},"pagination":{"totalCount":2,"pageCount":1,"currentPage":1,"perPage":10}}'

        voice_recordings = Client('', http_client).voice_recording_list_recordings('12348765-4321-0987-6543-210987654321', '87654321-0987-6543-2109-876543210987')

        http_client.request.assert_called_once_with('https://voice.messagebird.com/calls/12348765-4321-0987-6543-210987654321/legs/87654321-0987-6543-2109-876543210987/recordings', 'GET', None)

        recordings_check = {
            '12345678-9012-3456-7890-123456789012': { "id": '12345678-9012-3456-7890-123456789012', "duration": 32, "year": 2018 },
            '12345678-9012-3456-7890-123456789013': { "id": '12345678-9012-3456-7890-123456789013', "duration": 12, "year": 2019 }
        }

        for item in voice_recordings._items:
            recording_specific = recordings_check.get(item.id)
            self.assertEqual(recording_specific['id'], item.id)
            self.assertEqual(recording_specific['duration'], item.duration)
            self.assertEqual('done', item.status)
            self.assertEqual('wav', item.format)
            self.assertEqual(datetime(recording_specific['year'], 1, 1, 0, 0, 1), item.createdAt)
            self.assertEqual(datetime(recording_specific['year'], 1, 1, 0, 0, 5), item.updatedAt)
            self.assertEqual(2, len(item._links))

if __name__ == '__main__':
    unittest.main()
