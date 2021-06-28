import unittest
from unittest.mock import Mock

from messagebird import Client


class TestMMS(unittest.TestCase):

    def test_create_mms(self):
        http_client = Mock()
        http_client.request.return_value = '{"originator": "test-org", "body": "Rich test message", "direction": "mt", "recipients": {"totalCount": 1, "totalSentCount": 1, "totalDeliveredCount": 0, "totalDeliveryFailedCount": 0, "items": [{"status": "sent", "statusDatetime": "2019-06-04T13:54:48+00:00", "recipient": 4915238456487}]}, "reference": null, "createdDatetime": "2019-06-04T13:54:48+00:00", "href": "https://rest.messagebird.com/mms/0a75f8f82b5d4377bd8fb5b22ac1e8ac", "mediaUrls": ["https://www.messagebird.com/assets/images/og/messagebird.gif"], "scheduledDatetime": null, "id": "0a75f8f82b5d4377bd8fb5b22ac1e8ac", "subject": null}'

        params = {
            "originator": "test-org",
            "body": "Rich test message",
            "recipients": "+4915238456487",
            "mediaUrls": "https://www.messagebird.com/assets/images/og/messagebird.gif"
        }
        mms = Client('', http_client).mms_create(**params)

        params["mediaUrls"] = [params["mediaUrls"]]
        params.update({'subject': None, 'reference': None, 'scheduledDatetime': None})
        http_client.request.assert_called_once_with('mms', 'POST', params)

        self.assertEqual(params["originator"], mms.originator)
        self.assertEqual(params["recipients"].strip("+"), str(mms.recipients["items"][0].recipient))
        self.assertEqual(1, len(mms.recipients["items"]))
