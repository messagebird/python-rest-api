import json
import unittest
from messagebird import Client, ErrorException
from messagebird.base import Base

try:
    from unittest.mock import Mock
except ImportError:
    # mock was added to unittest in Python 3.3, but was an external library
    # before.
    from mock import Mock


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
                "title": "Say message",
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

        http_client.request.assert_called_once_with('calls', 'POST', params)

        # check all api response data is outputted
        expected_data = self.create_expected_call_data_based_on_api_response(api_response)
        response_data = call_creation_response.data.__dict__
        self.assertEqual(expected_data, response_data, 'Check client response contains the api response data.')

        # check it can be formatted as string
        expected_call_string = 'id                 : None\n' + \
            'data.id                 : 21025ed1-cc1d-4554-ac05-043fa6c84e00\n' + \
            'data.updatedAt          : 2017-08-30 07:35:37+00:00\n' + \
            'data.createdAt          : 2017-08-30 07:35:37+00:00\n' + \
            'data.endedAt            : None\n' + \
            'data.webhook            : None'
        self.assertEqual(expected_call_string, str(call_creation_response), 'Check returned call can be formatted as' +
                         'string')

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
