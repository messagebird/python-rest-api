import unittest
from unittest.mock import Mock

from messagebird import Client


class TestLookup(unittest.TestCase):

    def test_lookup(self):
        http_client = Mock()
        http_client.request.return_value = '{"href": "https://rest.messagebird.com/lookup/31612345678","countryCode": "NL","countryPrefix": 31,"phoneNumber": 31612345678,"type": "mobile","formats": {"e164": "+31612345678","international": "+31 6 12345678","national": "06 12345678","rfc3966": "tel:+31-6-12345678"},"hlr": {"id": "hlr-id","network": 20416,"reference": "reference2000","status": "active","createdDatetime": "2015-12-15T08:19:24+00:00","statusDatetime": "2015-12-15T08:19:25+00:00"}}'

        lookup = Client('', http_client).lookup('0612345678', {'countryCode': 'NL'})

        http_client.request.assert_called_once_with('lookup/0612345678', 'GET', {'countryCode': 'NL'})

        self.assertEqual('mobile', lookup.type)

    def test_lookup_hlr(self):
        http_client = Mock()
        http_client.request.return_value = '{"id": "hlr-id","network": 20416,"reference": "reference2000","status": "active","createdDatetime": "2015-12-15T08:19:24+00:00","statusDatetime": "2015-12-15T08:19:25+00:00"}'

        lookup_hlr = Client('', http_client).lookup_hlr(31612345678, {'reference': 'reference2000'})

        http_client.request.assert_called_once_with('lookup/31612345678/hlr', 'GET', {'reference': 'reference2000'})

        self.assertEqual(lookup_hlr.status, 'active')

    def test_lookup_hlr_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).lookup_hlr_create(31612345678, {'reference': 'MyReference'})

        http_client.request.assert_called_once_with('lookup/31612345678/hlr', 'POST', {'reference': 'MyReference'})
