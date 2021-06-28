import requests
from enum import Enum

from messagebird.serde import json_serialize

from urllib.parse import urljoin


class ResponseFormat(Enum):
    text = 1
    binary = 2


class HttpClient:
    """Used for sending simple HTTP requests."""

    def __init__(self, endpoint, access_key, user_agent):
        self.__supported_status_codes = [200, 201, 204, 401, 404, 405, 422]

        self.endpoint = endpoint
        self.access_key = access_key
        self.user_agent = user_agent

    def request(self, path, method='GET', params=None, format=ResponseFormat.text):
        """Builds a request and gets a response."""
        if params is None:
            params = {}
        url = urljoin(self.endpoint, path)
        headers = {
            'Accept': 'application/json',
            'Authorization': 'AccessKey ' + self.access_key,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json; charset=UTF-8'
        }

        method_switcher = {
            'DELETE': lambda: requests.delete(url, verify=True, headers=headers, data=json_serialize(params)),
            'GET': lambda: requests.get(url, verify=True, headers=headers, params=params),
            'PATCH': lambda: requests.patch(url, verify=True, headers=headers, data=json_serialize(params)),
            'POST': lambda: requests.post(url, verify=True, headers=headers, data=json_serialize(params)),
            'PUT': lambda: requests.put(url, verify=True, headers=headers, data=json_serialize(params))
        }
        if method not in method_switcher:
            raise ValueError(str(method) + ' is not a supported HTTP method')

        response = method_switcher[method]()

        if response.status_code not in self.__supported_status_codes:
            response.raise_for_status()

        response_switcher = {
            ResponseFormat.text: response.text,
            ResponseFormat.binary: response.content
        }
        return response_switcher.get(format)
