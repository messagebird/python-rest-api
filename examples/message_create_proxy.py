#!/usr/bin/env python

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

ACCESS_KEY = 'test_gshuPaZoeEG6ovbc8M79w0QyM'

proxies = {
  'http': 'http://my.example.proxy:8765',
  'https': 'http://my.secure.example.proxy:9876'
}

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY, proxies=proxies)

  # Send a new message.
  msg = client.message_create('FromMe', '31612345678', 'Hello World', { 'reference' : 'Foobar' })

  # Print the object information.
  print('\nThe following information was returned as a Message object:\n')
  print('  id                : %s' % msg.id)
  print('  href              : %s' % msg.href)
  print('  direction         : %s' % msg.direction)
  print('  type              : %s' % msg.type)
  print('  originator        : %s' % msg.originator)
  print('  body              : %s' % msg.body)
  print('  reference         : %s' % msg.reference)
  print('  validity          : %s' % msg.validity)
  print('  gateway           : %s' % msg.gateway)
  print('  typeDetails       : %s' % msg.typeDetails)
  print('  datacoding        : %s' % msg.datacoding)
  print('  mclass            : %s' % msg.mclass)
  print('  scheduledDatetime : %s' % msg.scheduledDatetime)
  print('  createdDatetime   : %s' % msg.createdDatetime)
  print('  recipients        : %s\n' % msg.recipients)
  print()

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Message object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
