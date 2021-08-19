#!/usr/bin/env python
import argparse
import messagebird
from messagebird.error import ValidationError

parser = argparse.ArgumentParser()
parser.add_argument('--signingKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--signature', help='the signature', type=str, required=True)
parser.add_argument('--requestURL', help='the full request url', type=str, required=True)
parser.add_argument('--requestBody', help='the request body', type=str, required=True)
args = vars(parser.parse_args())

request_validator = messagebird.RequestValidator(args['signingKey'])

try:
    request_validator.validate_signature(args['signature'], args['requestURL'], args['requestBody'])
except ValidationError as err:
    print("The signed request cannot be verified: ", str(err))
