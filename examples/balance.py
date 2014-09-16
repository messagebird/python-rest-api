#!/usr/bin/env python

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

ACCESS_KEY = 'test_gshuPaZoeEG6ovbc8M79w0QyM'

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Fetch the Balance object.
  balance = client.balance()

  # Print the object information.
  print('\nThe following information was returned as a Balance object:\n')
  print('  amount  : %d' % balance.amount)
  print('  type    : %s' % balance.type)
  print('  payment : %s\n' % balance.payment)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Balance object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
