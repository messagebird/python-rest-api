#!/usr/bin/env python
import os
import sys
import argparse
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='Access key for MessageBird API.', type=str, required=True)
parser.add_argument('--limit', help='Limit the amount of results per page.', type=int, required=False, default=20)
parser.add_argument('--offset', help='Skip first n results.', type=int, required=False, default=0)
parser.add_argument('--features', help='Features for which search is done.', type=str, required=False, default=None)
parser.add_argument('--tags', help='Tags for which search is done.', type=str, required=False, default=None)
parser.add_argument('--number', help='Fragment of number.', type=str, required=False, default=None)
parser.add_argument('--region', help='Fragment of region data.', type=str, required=False, default=None)
parser.add_argument('--locality', help='Fragment of locality data.', type=str, required=False, default=None)
parser.add_argument('--type', help='Number type.', type=str, required=False, default=None)
args = vars(parser.parse_args())

try:
    # Create a MessageBird client with the specified accessKey.
    client = messagebird.Client(args['accessKey'])
    del(args['accessKey'])

    limit = 20
    offset = 0
    if args['limit'] is not None:
        limit = args['limit']
        del(args['limit'])
    if args['offset'] is not None:
        offset = args['offset']
        del(args['offset'])

    # Fetching all purchased phone numbers.
    numbers = client.purchased_numbers_list(args, limit, offset)

    # Print the object information.
    print('\nThe following information was returned as a %s object:\n' % numbers.__class__)
    if numbers.items is not None:
        print('  Containing the the following items:')
        for item in numbers.items:
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


