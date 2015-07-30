#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

ACCESS_KEY = 'test_gshuPaZoeEG6ovbc8M79w0QyM'

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Send a new voice message.
  vmsg = client.voice_message_create('31612345678', 'Hello World', { 'reference' : 'Foobar' })

  # Print the object information.
  print('\nThe following information was returned as a VoiceMessage object:\n')
  print('  id                : %s' % vmsg.id)
  print('  href              : %s' % vmsg.href)
  print('  originator        : %s' % vmsg.originator)
  print('  body              : %s' % vmsg.body)
  print('  reference         : %s' % vmsg.reference)
  print('  language          : %s' % vmsg.language)
  print('  voice             : %s' % vmsg.voice)
  print('  repeat            : %s' % vmsg.repeat)
  print('  ifMachine         : %s' % vmsg.ifMachine)
  print('  scheduledDatetime : %s' % vmsg.scheduledDatetime)
  print('  createdDatetime   : %s' % vmsg.createdDatetime)
  print('  recipients        : %s\n' % vmsg.recipients)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a VoiceMessage object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
