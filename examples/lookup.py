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
  print('You need to set an PHONE_NUMBER constant in this file')
  sys.exit(1)

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Fetch the Lookup object for the specified PHONE_NUMBER.
  lookup = client.lookup(PHONE_NUMBER)

  # Print the object information.
  print('\nThe following information was returned as a Lookup object:\n')
  print('  href                  : %s' % lookup.href)
  print('  phoneNumber           : %d' % lookup.phoneNumber)
  print('  countryCode           : %s' % lookup.countryCode)
  print('  countryPrefix         : %d' % lookup.countryPrefix)
  print('  type                  : %s' % lookup.type)
  print('  formats.e164          : %s' % lookup.formats.e164)
  print('  formats.international : %s' % lookup.formats.international)
  print('  formats.national      : %s' % lookup.formats.national)
  print('  formats.rfc3966       : %s' % lookup.formats.rfc3966)

  if lookup.hlr is not None:
    print('  hlr.id                : %s' % lookup.hlr.id)
    print('  hlr.network           : %d' % lookup.hlr.network)
    print('  hlr.reference         : %s' % lookup.hlr.reference)
    print('  hlr.status            : %s' % lookup.hlr.status)
    print('  hlr.createdDatetime   : %s' % lookup.hlr.createdDatetime)
    print('  hlr.statusDatetime    : %s' % lookup.hlr.statusDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Lookup object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
