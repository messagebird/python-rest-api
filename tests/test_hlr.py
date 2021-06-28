import unittest
from unittest.mock import Mock

from messagebird import Client


class TestHLR(unittest.TestCase):

    def test_hlr(self):
        http_client = Mock()
        http_client.request.return_value = '{"id":"hlr-id","href":"https://rest.messagebird.com/hlr/hlr-id","msisdn":31612345678,"network":20406,"reference":"MyReference","status": "sent","createdDatetime": "2015-01-04T13:14:08+00:00","statusDatetime": "2015-01-04T13:14:09+00:00"}'

        hlr = Client('', http_client).hlr('hlr-id')

        http_client.request.assert_called_once_with('hlr/hlr-id', 'GET', None)

        self.assertEqual('hlr-id', hlr.id)

    def test_hlr_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).hlr_create(31612345678, 'MyReference')

        http_client.request.assert_called_once_with('hlr', 'POST', {'msisdn': 31612345678, 'reference': 'MyReference'})
