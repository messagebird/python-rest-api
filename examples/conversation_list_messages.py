#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''
# CONVERSATION_ID = ''

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

  itemIds = []
  for msgItem in msg.items:
    itemIds.append(msgItem.id)

  # Print the object information.
  print('\nThe following information was returned as a Conversation Message List object:\n')
  print('  message ids  : %s' % itemIds)
  print('  offset       : %s' % msg.offset)
  print('  limit        : %s' % msg.limit)
  print('  totalCount   : %s' % msg.totalCount)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Conversation Message List object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
