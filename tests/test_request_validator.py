import json
import re
from unittest import mock
from pathlib import Path

import pytest as pytest

from messagebird.base import Base
from messagebird.error import ValidationError
from messagebird.request_validator import RequestValidator

ERROR_MAP = {
    "invalid jwt: claim nbf is in the future": "The token is not yet valid (nbf)",
    "invalid jwt: claim exp is in the past": "Signature has expired",
    "invalid jwt: signature is invalid": "Signature verification failed",
    "invalid jwt: signing method none is invalid": "The specified alg value is not allowed"
}


def load_test_cases():
    test_data_file = Path(__file__).parent / 'test_request_validator/webhook_signature_test_data.json'
    with open(test_data_file) as f:
        tc_data = json.loads(f.read())

    return tc_data


@mock.patch('jwt.api_jwt.datetime')
@pytest.mark.parametrize('test_case', load_test_cases(), ids=lambda args: args['name'])
def test_validate_signature(mock_dt, test_case):
    mock_dt.utcnow = mock.Mock(return_value=Base.value_to_time(test_case['timestamp']))

    validator = RequestValidator(test_case.get('secret'))

    payload = test_case.get('payload')
    if payload:
        payload = bytes(payload.encode())

    def run_decode():
        return validator.validate_signature(test_case['token'], test_case['url'], payload)

    if not test_case['valid']:
        err = ERROR_MAP.get(test_case["reason"]) or test_case["reason"]
        pytest.raises(ValidationError, run_decode).match(re.escape(err))
        return

    decoded = run_decode()

    assert decoded is not None
