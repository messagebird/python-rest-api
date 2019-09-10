#!/usr/bin/env python
import os
import sys
import argparse
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import messagebird


parser = argparse.ArgumentParser(usage='call_create.py\
 --accessKey="*******" \
 --page=1 \
')
parser.add_argument('--accessKey', help='Access key for MessageBird API.', type=str, required=True)
parser.add_argument('--page', help='The page you wish to view.', type=str, required=False, default=1)
args = vars(parser.parse_args())

try:
    # Create a MessageBird client with the specified accessKey.
    client = messagebird.Client(args['accessKey'])
    del(args['accessKey'])

    # Create a call for the specified callID.
    callList = client.call_list(**args)

    # Print the object information.
    print('\nThe following information was returned as a %s object:\n' % callList.__class__)
    if callList.items is not None:
        print('  Containing the the following items:')
        for item in callList.items:
            print('  {')
            print('    id                : %s' % item.id)
            print('    status            : %s' % item.status)
            print('    source            : %s' % item.source)
            print('    destination       : %s' % item.destination)
            print('    createdAt         : %s' % item.createdAt)
            print('    updatedAt         : %s' % item.updatedAt)
            print('    endedAt           : %s' % item.endedAt)
            print('  },')
    else:
        print('  With an empty response.')

except messagebird.client.ErrorException as e:
    print('\nAn error occurred while listing calls:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s' % error.parameter)
        print('  type        : %s' % error.__class__)

except requests.exceptions.HTTPError as e:
    print('\nAn HTTP exception occurred while listing calls:')
    print(' ', e)
    print('  Http request body: ', e.request.body)
    print('  Http response status: ', e.response.status_code)
    print('  Http response body: ', e.response.content.decode())

except Exception as e:
    print('\nAn ', e.__class__, ' exception occurred while creating a call:')
    print(e)


