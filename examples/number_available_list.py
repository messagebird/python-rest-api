#!/usr/bin/env python

import sys, os, argparse, requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
args = vars(parser.parse_args())

try:
  # Create a MessageBird client with the specified accessKey.
  client = messagebird.Client(args['accessKey'])

  # Fetch the NumberList object with specified params, limit, offset.
  params = {'features': ['sms', 'voice'], 'number': 319}
  numbers = client.available_numbers_list('NL', params, 2, 0)

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
