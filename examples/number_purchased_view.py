#!/usr/bin/env python
import os
import sys
import argparse
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='Access key for MessageBird API.', type=str, required=True)
parser.add_argument('--phoneNumber', help='Phone number.', type=str, required=True)
args = vars(parser.parse_args())

try:
    # Create a MessageBird client with the specified accessKey.
    client = messagebird.Client(args['accessKey'])

    # Fetching all purchased phone numbers.
    item = client.purchased_number(args['phoneNumber'])

    # Print the object information.
    print('\nThe following information was returned as a %s object:\n' % item.__class__)
    if item is not None:
        print('  {')
        print('    number                : %s' % item.number)
        print('    country               : %s' % item.country)
        print('    region                : %s' % item.region)
        print('    locality              : %s' % item.locality)
        print('    features              : %s' % item.features)
        print('    tags                  : %s' % item.tags)
        print('    type                  : %s' % item.type)
        print('    status                : %s' % item.status)
        print('  },')
    else:
        print('  With an empty response.')

except messagebird.client.ErrorException as e:
    print('\nAn error occurred while fetching all purchased phone numbers:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s' % error.parameter)
        print('  type        : %s' % error.__class__)

except requests.exceptions.HTTPError as e:
    print('\nAn HTTP exception occurred while fetching all purchased phone numbers:')
    print(' ', e)
    print('  Http request body: ', e.request.body)
    print('  Http response status: ', e.response.status_code)
    print('  Http response body: ', e.response.content.decode())

except Exception as e:
    print('\nAn ', e.__class__, ' exception occurred while :')
    print(e)



