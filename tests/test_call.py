import unittest
from messagebird import Client, ErrorException

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


class TestCall(unittest.TestCase):

    def test_call(self):
        http_client = Mock()
        http_client.request.return_value = '{"data":[{"id":"call-id","status":"ended","source":"16479311111","destination":"1416555555","createdAt":"2019-08-06T13:17:06Z","updatedAt":"2019-08-06T13:17:39Z","endedAt":"2019-08-06T13:17:39Z"}],"_links":{"legs":"/calls/66bd9f08-a8af-40fe-a830-652d8dabc057/legs","self":"/calls/66bd9f08-a8af-40fe-a830-652d8bca357"},"pagination":{"totalCount":0,"pageCount":0,"currentPage":0,"perPage":0}}'

        call = Client('', http_client).call('call-id')

        http_client.request.assert_called_once_with('calls/call-id', 'GET', None)

        self.assertEqual('ended', call.data.status)