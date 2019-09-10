#!/usr/bin/env python
import os
import sys
import json
import argparse
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import messagebird

parser = argparse.ArgumentParser(usage='call_create.py\
 --accessKey="*******" \
 --callId=dda20377-72da-4846-9b2c-0fea3ad4bcb6 \
')
parser.add_argument('--accessKey', help='Access key for MessageBird API.', type=str, required=True)
parser.add_argument('--callId', help='The ID of the MessageBird call to delete.', type=str, required=True)
args = vars(parser.parse_args())

try:
    # Create a MessageBird client with the specified accessKey.
    client = messagebird.Client(args['accessKey'])

    # Create a call for the specified callID.
    call = client.call_delete(args['callId'])

    # If no error is thrown, means delete was successful.
    print('\nDeleted call with id `%s` successfully!' % args['callId'])

except messagebird.client.ErrorException as e:
    print('\nAn error occurred while creating a call:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s' % error.parameter)
        print('  type        : %s' % error.__class__)

except requests.exceptions.HTTPError as e:
    print('\nAn http exception occurred while deleting a call:')
    print(' ', e)
    print('  Http request body: ', e.request.body)
    print('  Http response status: ', e.response.status_code)
    print('  Http response body: ', e.response.content.decode())

except Exception as e:
    print('\nAn ', e.__class__, ' exception occurred while deleting a call:')
    print(e)

