#!/usr/bin/env python

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''
# MESSAGE_ID = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  MESSAGE_ID
except NameError:
  print('You need to set a MESSAGE_ID constant in this file')
  sys.exit(1)

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Fetch the VoiceMessage object for the specified MESSAGE_ID.
  vmsg = client.voice_message(MESSAGE_ID)

  # Print the object information.
  print('\nThe following information was returned as a VoiceMessage object:\n')
  print('  id                : %s' % vmsg.id)
  print('  href              : %s' % vmsg.href)
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
