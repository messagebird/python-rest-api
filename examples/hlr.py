#!/usr/bin/env python

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''
# HLR_ID = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  HLR_ID
except NameError:
  print('You need to set an HLR_ID constant in this file')
  sys.exit(1)

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Fetch the HLR lookup object for the specified HLR_ID.
  hlr = client.hlr(HLR_ID)

  # Print the object information.
  print('\nThe following information was returned as an HLR object:\n')
  print('  id              : %s' % hlr.id)
  print('  href            : %s' % hlr.href)
  print('  msisdn          : %s' % hlr.msisdn)
  print('  reference       : %s' % hlr.reference)
  print('  status          : %s' % hlr.status)
  print('  createdDatetime : %s' % hlr.createdDatetime)
  print('  statusDatetime  : %s\n' % hlr.statusDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting an HLR object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
