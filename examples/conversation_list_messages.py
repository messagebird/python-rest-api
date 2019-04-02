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
  CONVERSATION_ID
except NameError:
  print('You need to set a CONVERSATION_ID constant in this file')
  sys.exit(1)

try:
  client = messagebird.ConversationClient(ACCESS_KEY)

  msg = client.list_messages(CONVERSATION_ID)

  # Print the object information.
  print(msg)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Message object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
