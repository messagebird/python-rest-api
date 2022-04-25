import json
import unittest
from unittest.mock import Mock

from messagebird import Client
from messagebird.base import Base


class TestCall(unittest.TestCase):

    def test_call(self):
        http_client = Mock()
        http_client.request.return_value = """
            {
               "data":[
                  {
                     "id":"call-id",
                     "status":"ended",
                     "source":"16479311111",
                     "destination":"1416555555",
                     "createdAt":"2019-08-06T13:17:06Z",
                     "updatedAt":"2019-08-06T13:17:39Z",
                     "endedAt":"2019-08-06T13:17:39Z"
                  }
               ],
               "_links":{
                  "legs":"/calls/66bd9f08-a8af-40fe-a830-652d8dabc057/legs",
                  "self":"/calls/66bd9f08-a8af-40fe-a830-652d8bca357"
               },
               "pagination":{
                  "totalCount":0,
                  "pageCount":0,
                  "currentPage":0,
                  "perPage":0
               }
            }
            """

        call = Client('', http_client).call('call-id')

        http_client.request.assert_called_once_with('calls/call-id', 'GET', None)

        self.assertEqual('ended', call.data.status)

    def test_call_list(self):
        http_client = Mock()
        http_client.request.return_value = """
            {
               "data":[
                  {
                     "id":"dda20377-72da-4846-9b2c-0fea3ad4bcb6",
                     "status":"no_answer",
                     "source":"16479311111",
                     "destination":"1416555555",
                     "createdAt":"2019-08-06T13:17:06Z",
                     "updatedAt":"2019-08-06T13:17:39Z",
                     "endedAt":"2019-08-06T13:17:39Z",
                     "_links":{
                       "legs":"/calls/dda20377-72da-4846-9b2c-0fea3ad4bcb6/legs",
                       "self":"/calls/dda20377-72da-4846-9b2c-0fea3ad4bcb6"
                     }
                  },
                  {
                     "id":"1541535b-9b80-4002-bde5-ed05b5ebed76",
                     "status":"ended",
                     "source":"16479311111",
                     "destination":"1416555556",
                     "createdAt":"2019-08-06T13:17:06Z",
                     "updatedAt":"2019-08-06T13:17:39Z",
                     "endedAt":"2019-08-06T13:17:39Z",
                     "_links":{
                       "legs":"/calls/1541535b-9b80-4002-bde5-ed05b5ebed76/legs",
                       "self":"/calls/1541535b-9b80-4002-bde5-ed05b5ebed76"
                     }
                  }
               ],
               "_links": {
                   "self": "/calls?page=1"
               },
               "pagination":{
                  "totalCount":2,
                  "pageCount":1,
                  "currentPage":1,
                  "perPage":10
               }
            }
            """

        callList = Client('', http_client).call_list(page=1)

        http_client.request.assert_called_once_with('calls/?page=1', 'GET', None)

        # check data is processed
        self.assertEqual('no_answer', callList.data[0].status)
        self.assertEqual('ended', callList.data[1].status)

        # check pagination is passed to object
        self.assertEqual(2, callList.totalCount)
        self.assertEqual(1, callList.pageCount)
        self.assertEqual(1, callList.currentPage)
        self.assertEqual(10, callList.perPage)
        self.assertEqual(10, callList.pagination['perPage'], 'Check it also supports API pagination format.')

        self.assertEqual(0, callList.offset, 'Check it correctly calculates offset.')
        self.assertEqual(10, callList.limit, 'Check it correctly calculates limit.')

    def test_call_create(self):
        api_response = {
            "data": [
                {
                    "id": "21025ed1-cc1d-4554-ac05-043fa6c84e00",
                    "status": "queued",
                    "source": "31644556677",
                    "destination": "31612345678",
                    "createdAt": "2017-08-30T07:35:37Z",
                    "updatedAt": "2017-08-30T07:35:37Z",
                    "endedAt": None
                }
            ],
            "_links": {
                "self": "/calls/21025ed1-cc1d-4554-ac05-043fa6c84e00"
            }
        }

        params = {
            "source": "31644556677",
            "destination": "31612345678",
            "callFlow": {
                "steps": [
                    {
                        "action": "say",
                        "options": {
                            "payload": "This is a journey into sound. Good bye!",
                            "voice": "male",
                            "language": "en-US"
                        }
                    }
                ]
            },
            "webhook": {
                "url": "https://example.com",
                "token": "token_to_sign_the_call_events_with",
            }
        }

        http_client = Mock()
        http_client.request.return_value = json.dumps(api_response)

        call_creation_response = Client('', http_client).call_create(**params)

        http_client.request.assert_called_once_with('calls/', 'POST', params)

        # check all api response data is outputted
        expected_data = self.create_expected_call_data_based_on_api_response(api_response)
        response_data = call_creation_response.data.__dict__
        self.assertEqual(expected_data, response_data, 'Check client response contains the API response data.')

        # check it can be formatted as string
        self.assertTrue(len(str(call_creation_response)) > 0, 'Check returned call can be formatted as string.')

    def test_call_delete(self):
        http_client = Mock()
        http_client.request.return_value = ''
        call_id_to_delete = '21025ed1-cc1d-4554-ac05-043fa6c84e00'
        Client('', http_client).call_delete(call_id_to_delete)

        http_client.request.assert_called_once_with('calls/%s' % call_id_to_delete, 'DELETE', None)

    @staticmethod
    def create_expected_call_data_based_on_api_response(api_response):
        expected_data = api_response['data'][0]

        # convert dates
        expected_data['_createdAt'] = Base.value_to_time(expected_data['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
        expected_data['_updatedAt'] = Base.value_to_time(expected_data['updatedAt'], '%Y-%m-%dT%H:%M:%SZ')
        expected_data['_endedAt'] = Base.value_to_time(expected_data['endedAt'], '%Y-%m-%dT%H:%M:%SZ')
        del (expected_data['createdAt'], expected_data['updatedAt'], expected_data['endedAt'])

        # add generated data
        expected_data.setdefault('_webhook', None)

        return expected_data
