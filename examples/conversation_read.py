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
  print('You need to set an CONVERSATION_ID constant in this file')
  sys.exit(1)

try:
  client = messagebird.ConversationClient(ACCESS_KEY)

  conversation = client.read(CONVERSATION_ID)

  # Print the object information.
  print('\nThe following information was returned as a Conversation object:\n')
  print('  conversation id           : %s' % conversation.id)
  print('  contact id                : %s' % conversation.contactId)
  print('  messages total count      : %s' % conversation.messages.totalCount)
  print('  status                    : %s' % conversation.status)
  print('  created date time         : %s' % conversation.createdDatetime)
  print('  updated date time         : %s' % conversation.updatedDatetime)
  print('  last received date time   : %s' % conversation.lastReceivedDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Conversation object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)