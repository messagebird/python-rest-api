#!/usr/bin/env python

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

ACCESS_KEY = 'test_gshuPaZoeEG6ovbc8M79w0QyM'

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Fetch the NumberList object.
  numbers = client.available_numbers_list(20, 0)

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
