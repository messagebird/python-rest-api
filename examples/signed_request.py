#!/usr/bin/env python
import sys
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--signingKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--requestTimestamp', help='the request timestamp', type=str, required=True)
parser.add_argument('--requestBody', help='the request body', type=str, required=True)
parser.add_argument('--signature', help='the signature', type=str, required=True)
args = vars(parser.parse_args())

signed_request = messagebird.SignedRequest(args['signature'], args['timestamp'], args['requestBody'], {})

if signed_request.verify(args['signingKey']):
    print("The signed request has been verified.")
else:
    print("The signed request cannot be verified.")

if signed_request.isRecent():
    print("The signed request is recent.")
else:
    print("The signed request is not recent.")