import unittest
from unittest.mock import Mock

from messagebird import Client


class TestGroup(unittest.TestCase):

    def test_group(self):
        http_client = Mock()
        http_client.request.return_value = '{"id": "group-id","href": "https://rest.messagebird.com/groups/group-id","name": "Friends","contacts": {"totalCount": 3,"href": "https://rest.messagebird.com/groups/group-id"},"createdDatetime": "2018-07-25T12:16:10+00:00","updatedDatetime": "2018-07-25T12:16:23+00:00"}'

        group = Client('', http_client).group('group-id')

        http_client.request.assert_called_once_with('groups/group-id', 'GET', None)

        self.assertEqual('Friends', group.name)
        self.assertEqual(3, group.contacts.totalCount)

    def test_group_create(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).group_create('Family', {'foo': 'bar'})

        http_client.request.assert_called_once_with('groups', 'POST', {'name': 'Family', 'foo': 'bar'})

    def test_group_delete(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).group_delete('group-id')

        http_client.request.assert_called_once_with('groups/group-id', 'DELETE', None)

    def test_list(self):
        http_client = Mock()
        http_client.request.return_value = '{"offset": 0,"limit": 25,"count": 2,"totalCount": 2,"links": {"first": "https://rest.messagebird.com/groups?offset=0&limit=10","previous": null,"next": null,"last": "https://rest.messagebird.com/groups?offset=0&limit=10"},"items": [{"id": "first-id","href": "https://rest.messagebird.com/groups/first-id","name": "First","contacts": {"totalCount": 3,"href": "https://rest.messagebird.com/groups/first-id/contacts"},"createdDatetime": "2018-07-25T11:47:42+00:00","updatedDatetime": "2018-07-25T14:03:09+00:00"},{"id": "second-id","href": "https://rest.messagebird.com/groups/second-id","name": "Second","contacts": {"totalCount": 4,"href": "https://rest.messagebird.com/groups/second-id/contacts"},"createdDatetime": "2018-07-25T11:47:39+00:00","updatedDatetime": "2018-07-25T14:03:09+00:00"}]}'

        group_list = Client('', http_client).group_list(limit=25, offset=0)

        http_client.request.assert_called_once_with('groups?limit=25&offset=0', 'GET', None)

        self.assertEqual(2, group_list.totalCount)
        self.assertEqual('https://rest.messagebird.com/groups?offset=0&limit=10', group_list.links.first)
        self.assertEqual('Second', group_list.items[1].name)

    def test_group_update(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).group_update('group-id', 'friends')

        http_client.request.assert_called_once_with('groups/group-id', 'PATCH', {'name': 'friends'})

    def test_group_add_contacts(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).group_add_contacts('group-id', ['contact-id', 'other-contact-id'])

        http_client.request.assert_called_once_with('groups/group-id?ids[]=contact-id&ids[]=other-contact-id', 'PUT',
                                                    None)

    def test_group_remove_contact(self):
        http_client = Mock()
        http_client.request.return_value = ''

        Client('', http_client).group_remove_contact('group-id', 'contact-id')

        http_client.request.assert_called_once_with('groups/group-id/contacts/contact-id', 'DELETE', None)
