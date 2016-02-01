#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''
# PHONE_NUMBER = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  PHONE_NUMBER
except NameError:
  print('You need to set a PHONE_NUMBER constant in this file')
  sys.exit(1)

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Create a new Lookup HLR object.
  lookup_hlr = client.lookup_hlr_create(PHONE_NUMBER, { 'reference' : 'Reference' })

  # Print the object information.
  print('\nThe following information was returned as a Lookup HLR object:\n')
  print('  id              : %s' % lookup_hlr.id)
  print('  href            : %s' % lookup_hlr.href)
  print('  msisdn          : %d' % lookup_hlr.msisdn)
  print('  reference       : %s' % lookup_hlr.reference)
  print('  status          : %s' % lookup_hlr.status)
  print('  details         : %s' % lookup_hlr.details)
  print('  createdDatetime : %s' % lookup_hlr.createdDatetime)
  print('  statusDatetime  : %s\n' % lookup_hlr.statusDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Lookup HLR object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
