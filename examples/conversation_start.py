#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird
from messagebird.conversation_message import MESSAGE_TYPE_TEXT

# ACCESS_KEY = ''
# CHANNEL_ID = ''
# PHONE_NUMBER = ''
# TEXT_MESSAGE = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  CHANNEL_ID
except NameError:
  print('You need to set a CHANNEL_ID constant in this file')
  sys.exit(1)

try:
  PHONE_NUMBER
except NameError:
  print('You need to set a PHONE_NUMBEr constant in this file')
  sys.exit(1)

try:
  TEXT_NUMBER
except NameError:
  print('You need to set a TEXT_NUMBER constant in this file')
  sys.exit(1)

try:
  client = messagebird.ConversationClient(ACCESS_KEY)

  msg = client.start({ 'channelId':  CHANNEL_ID, 'to': PHONE_NUMBER, 'type': MESSAGE_TYPE_TEXT, 'content': { 'text': TEXT_MESSAGE } })

  # Print the object information.
  print('\nThe following information was returned as a Conversation object:\n')
  print('  id                    : %s' % msg.id)
  print('  contact id            : %s' % msg.contactId)
  print('  contact               : %s' % msg.contact)
  print('  last used channel id  : %s' % msg.lastUsedChannelId)
  print('  channels              : %s' % msg.channels)
  print('  messages              : %s' % msg.messages)
  print('  status                : %s' % msg.status)
  print('  createdDateTime       : %s' % msg.createdDateTime)
  print('  updatedDateTime       : %s' % msg.updatedDateTime)
  print('  lastReceivedDateTime  : %s' % msg.lastReceivedDateTime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Message object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
