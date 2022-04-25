import unittest
from unittest.mock import Mock

from messagebird import Client


class TestCallFlow(unittest.TestCase):

    def test_get_flow(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "de3ed163-d5fc-45f4-b8c4-7eea7458c635",
              "title": "Updated call flow",
              "record": false,
              "steps": [
                {
                  "id": "3538a6b8-5a2e-4537-8745-f72def6bd393",
                  "action": "transfer",
                  "options": {
                    "destination": "31611223344"
                  }
                }
              ],
              "createdAt": "2017-03-06T13:34:14Z",
              "updatedAt": "2017-03-06T15:02:38Z"
            }
          ],
          "_links": {
            "self": "/call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c635"
          }
        }
        '''

        call_flow = Client('', http_client).call_flow('de3ed163-d5fc-45f4-b8c4-7eea7458c635')
        http_client.request.assert_called_once_with('call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c635', 'GET', None)

        self.assertEqual('Updated call flow', call_flow.title)
        self.assertIsNotNone(call_flow.steps)

    def test_get_flow_list(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "de3ed163-d5fc-45f4-b8c4-7eea7458c635",
              "record": false,
              "steps": [
                {
                  "id": "3538a6b8-5a2e-4537-8745-f72def6bd393",
                  "action": "transfer",
                  "options": {
                    "destination": "31612345678"
                  }
                }
              ],
              "createdAt": "2017-03-06T13:34:14Z",
              "updatedAt": "2017-03-06T13:34:14Z",
              "_links": {
                "self": "/call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c635"
              }
            },
            {
              "id": "de3ed163-d5fc-45f4-b8c4-7eea7458c634",
              "record": true,
              "steps": [
                {
                  "id": "3538a6b8-5a2e-4537-8745-f72def6bd393",
                  "action": "transfer",
                  "options": {
                    "destination": "31612345678"
                  }
                }
              ],
              "createdAt": "2017-03-06T13:34:14Z",
              "updatedAt": "2017-03-06T13:34:14Z",
              "_links": {
                "self": "/call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c634"
              }
            }
          ],
          "_links": {
            "self": "/call-flows?page=1"
          },
          "pagination": {
            "totalCount": 2,
            "pageCount": 2,
            "currentPage": 1,
            "perPage": 10
          }
        }
        '''

        call_flow_list = Client('', http_client).call_flow_list(20, 0)

        http_client.request.assert_called_once_with('call-flows?limit=20&offset=0', 'GET', None)
        self.assertEqual(call_flow_list.data[0].title, None)
        self.assertEqual(call_flow_list.data[1].title, None)

        self.assertEqual(2, call_flow_list.pagination['totalCount'])

    def test_numbers_list(self):
        http_client = Mock()
        http_client.request.return_value = '''{
          "data": [
            {
              "id": "13f38f34-7ff4-45b3-8783-8d5b1143f22b",
              "number": "31611111111",
              "callFlowId": "de3ed163-d5fc-45f4-b8c4-7eea7458c635",
              "createdAt": "2017-03-16T13:49:24Z",
              "updatedAt": "2017-09-12T08:59:50Z",
              "_links": {
                "self": "/numbers/13f38f34-7ff4-45b3-8783-8d5b1143f22b"
              }
            }
          ],
          "_links": {
            "self": "/call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c635/numbers?page=1"
          },
          "pagination": {
            "totalCount": 1,
            "pageCount": 1,
            "currentPage": 1,
            "perPage": 10
          }
        }
        '''

        number_list = Client('', http_client).call_flow_numbers_list('de3ed163-d5fc-45f4-b8c4-7eea7458c635')

        http_client.request.assert_called_once_with('call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c635/numbers', 'GET',
                                                    None)

        self.assertEqual('31611111111', number_list.data[0].number)
        self.assertEqual(1, number_list.pagination['totalCount'])

    def test_numbers_add(self):
        http_client = Mock()
        http_client.request.return_value = '{}'

        Client('', http_client).call_flow_numbers_add(
            'de3ed163-d5fc-45f4-b8c4-7eea7458c635',
            ['31611111111', '31611111112']
        )

        params = {'numbers': ['31611111111', '31611111112']}

        http_client.request.assert_called_once_with(
            'call-flows/de3ed163-d5fc-45f4-b8c4-7eea7458c635/numbers', 'POST', params)
