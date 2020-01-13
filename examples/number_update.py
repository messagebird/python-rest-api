#!/usr/bin/env python

import sys
import os
import argparse
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
args = vars(parser.parse_args())

try:
  # Create a MessageBird client with the specified accessKey.
  client = messagebird.Client(args['accessKey'])

  # Update number
  # Note: at the moment, we only support updating tags that can be used to group or label numbers
  tags = ['tag1']
  number = client.update_number('3197010240126', tags)

  # Print the object information.
  print('\nThe following information was returned as a Number object:\n')
  print('    number                : %s' % number.number)
  print('    country               : %s' % number.country)
  print('    region                : %s' % number.region)
  print('    locality              : %s' % number.locality)
  print('    features              : %s' % number.features)
  print('    tags                  : %s' % number.tags)
  print('    type                  : %s' % number.type)
  print('    status                : %s' % number.status)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a NumberList object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)

except requests.exceptions.HTTPError as e:
    print('\nAn HTTP exception occurred while fetching all purchased phone numbers:')
    print(' ', e)
    print('  Http request body: ', e.request.body)
    print('  Http response status: ', e.response.status_code)
    print('  Http response body: ', e.response.content.decode())

except Exception as e:
    print('\nAn ', e.__class__, ' exception occurred while :')
    print(e)
