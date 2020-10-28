import unittest
from unittest.mock import Mock

from messagebird import Client, ErrorException


class TestContact(unittest.TestCase):

    def test_contact(self):
        http_client = Mock()
        http_client.request.return_value = '{"id": "contact-id","href": "https://rest.messagebird.com/contacts/contact-id","msisdn": 31612345678,"firstName": "Foo","lastName": "Bar","customDetails": {"custom1": "First","custom2": "Second","custom3": "Third","custom4": "Fourth"},"groups": {"totalCount": 3,"href": "https://rest.messagebird.com/contacts/contact-id/groups"},"messages": {"totalCount": 5,"href": "https://rest.messagebird.com/contacts/contact-id/messages"},"createdDatetime": "2018-07-13T10:34:08+00:00","updatedDatetime": "2018-07-13T10:44:08+00:00"}'

        contact = Client('', http_client).contact('contact-id')

        http_client.request.assert_called_once_with('contacts/contact-id', 'GET', None)

        self.assertEqual(31612345678, contact.msisdn)
        self.assertEqual('First', contact.customDetails.custom1)
        self.assertEqual(3, contact.groups.totalCount)
        self.assertEqual('https://rest.messagebird.com/contacts/contact-id/messages', contact.messages.href)

    def test_contact_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).contact_create(31612345678, {'firstName': 'Foo', 'custom3': 'Third'})

        http_client.request.assert_called_once_with(
            'contacts', 'POST', {'msisdn': 31612345678, 'firstName': 'Foo', 'custom3': 'Third'})

    def test_contact_delete(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).contact_delete('contact-id')

        http_client.request.assert_called_once_with('contacts/contact-id', 'DELETE', None)

    def test_contact_delete_invalid(self):
        http_client = Mock()
        http_client.request.return_value = '{"errors": [{"code": 20,"description": "contact not found","parameter": null}]}'

        with self.assertRaises(ErrorException):
            Client('', http_client).contact_delete('non-existent-contact-id')

        http_client.request.assert_called_once_with('contacts/non-existent-contact-id', 'DELETE', None)

    def test_contact_update(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).contact_update('contact-id', {'msisdn': 31687654321, 'custom4': 'fourth'})

        http_client.request.assert_called_once_with(
            'contacts/contact-id', 'PATCH', {'msisdn': 31687654321, 'custom4': 'fourth'}
        )

    def test_contact_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"offset": 0,"limit": 20,"count": 2,"totalCount": 2,"links": {"first": "https://rest.messagebird.com/contacts?offset=0","previous": null,"next": null,"last": "https://rest.messagebird.com/contacts?offset=0"},"items": [{"id": "first-id","href": "https://rest.messagebird.com/contacts/first-id","msisdn": 31612345678,"firstName": "Foo","lastName": "Bar","customDetails": {"custom1": null,"custom2": null,"custom3": null,"custom4": null},"groups": {"totalCount": 0,"href": "https://rest.messagebird.com/contacts/first-id/groups"},"messages": {"totalCount": 0,"href": "https://rest.messagebird.com/contacts/first-id/messages"},"createdDatetime": "2018-07-13T10:34:08+00:00","updatedDatetime": "2018-07-13T10:34:08+00:00"},{"id": "second-id","href": "https://rest.messagebird.com/contacts/second-id","msisdn": 49612345678,"firstName": "Hello","lastName": "World","customDetails": {"custom1": null,"custom2": null,"custom3": null,"custom4": null},"groups": {"totalCount": 0,"href": "https://rest.messagebird.com/contacts/second-id/groups"},"messages": {"totalCount": 0,"href": "https://rest.messagebird.com/contacts/second-id/messages"},"createdDatetime": "2018-07-13T10:33:52+00:00","updatedDatetime": null}]}'

        contact_list = Client('', http_client).contact_list(10, 20)

        http_client.request.assert_called_once_with('contacts?limit=10&offset=20', 'GET', None)

        self.assertEqual(2, contact_list.totalCount)
        self.assertEqual('https://rest.messagebird.com/contacts?offset=0', contact_list.links.first)
        self.assertEqual('https://rest.messagebird.com/contacts/first-id/groups', contact_list.items[0].groups.href)
