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
  client = messagebird.Client(ACCESS_KEY)

  msg = client.conversation_read_message(MESSAGE_ID)

  # Print the object information.
  print('\nThe following information was returned as a Conversation List object:\n')
  print('  message id   : %s' % msg.id)
  print('  channel id   : %s' % msg.channelId)
  print('  direction    : %s' % msg.direction)
  print('  content      : %s' % msg.content)
  print('  content      : %s' % msg.content)
  print('  status       : %s' % msg.status)
  print('  type         : %s' % msg.type)
  print('  created date : %s' % msg.createdDatetime)
  print('  updated date : %s' % msg.updatedDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Message object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
