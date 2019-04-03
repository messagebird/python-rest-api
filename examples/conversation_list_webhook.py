#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  client = messagebird.ConversationClient(ACCESS_KEY)

  webhookList = client.list()

  itemIds = []
  for msgItem in webhookList.items:
    itemIds.append(msgItem.id)

  # Print the object information.
  print('\nThe following information was returned as a Conversation Webhook List object:\n')
  print('  conversation ids  : %s' % itemIds)
  print('  offset       : %s' % webhookList.offset)
  print('  limit        : %s' % webhookList.limit)
  print('  totalCount   : %s' % webhookList.totalCount)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Conversation Webhook List object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)