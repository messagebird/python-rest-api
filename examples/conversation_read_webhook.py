#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''
# WEBHOOK_ID = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  WEBHOOK_ID
except NameError:
  print('You need to set an WEBHOOK_ID constant in this file')
  sys.exit(1)

try:
  client = messagebird.Client(ACCESS_KEY)

  webhook = client.conversation_read_webhook(WEBHOOK_ID)

  # Print the object information.
  print('\nThe following information was returned as a Webhook object:\n')
  print('  id            : %s' % webhook.id)
  print('  events        : %s' % webhook.events)
  print('  channel id    : %s' % webhook.channelId)
  print('  created date  : %s' % webhook.createdDatetime)
  print('  updated date  : %s' % webhook.updatedDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Webhook object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)