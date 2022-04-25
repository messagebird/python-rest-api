#!/usr/bin/env python
import os
import sys
import json
import argparse
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import messagebird

exampleCallFlow = '{"steps":[{"action":"say","options":{"payload":"Hey, this is your first voice \
call","language":"en-GB","voice":"female"}}]}'

parser = argparse.ArgumentParser(usage='call_create.py\
 --accessKey="*******" \
 --destination=31612345678 \
 --source=31644556677 \
 --callFlow \'' + exampleCallFlow + '\'\
')
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--source', help='The caller ID of the call.', type=str, required=True)
parser.add_argument('--destination', help='The number/address to be called.', type=str, required=True)
parser.add_argument('--callFlow', help='The call flow object to be executed when the call is answered.', type=str, required=False, default=exampleCallFlow)
parser.add_argument('--webhook', help='The webhook object containing the url & required token.', type=str, required=False, default='{}')
args = vars(parser.parse_args())

# arguments to parse as json
jsonArgs = ['callFlow', 'webhook']

for jsonArg in jsonArgs:
    try:
        args[jsonArg] = json.loads(str(args[jsonArg]).strip('\''))
    except json.decoder.JSONDecodeError as e:
        parser.print_usage()
        print('Invalid json provided for %s: %s' % (jsonArg, e))
        print('Provided %s json: %s' % (jsonArg, args[jsonArg]))
        exit(1)

try:
    # Create a MessageBird client with the specified accessKey.
    client = messagebird.Client(args['accessKey'])
    del(args['accessKey'])

    # Create a call for the specified callID.
    call = client.call_create(**args)

    # Print the object information.
    print('\nThe following information was returned as a', str(call.__class__), 'object:\n')
    print('  id                : %s' % call.data.id)
    print('  status            : %s' % call.data.status)
    print('  source            : %s' % call.data.source)
    print('  destination       : %s' % call.data.destination)
    print('  webhook           : %s' % call.data.webhook)
    print('  createdAt         : %s' % call.data.createdAt)
    print('  updatedAt         : %s' % call.data.updatedAt)
    print('  endedAt           : %s' % call.data.endedAt)

except messagebird.client.ErrorException as e:
    print('\nAn error occurred while creating a call:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s' % error.parameter)
        print('  type        : %s' % error.__class__)

except requests.exceptions.HTTPError as e:
    print('\nAn http exception occurred while creating a call:')
    print(' ', e)
    print('  Http request body: ', e.request.body)
    print('  Http response status: ', e.response.status_code)
    print('  Http response body: ', e.response.content.decode())

except Exception as e:
    print('\nAn ', e.__class__, ' exception occurred while creating a call:')
    print(e)

