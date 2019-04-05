#!/usr/bin/env python
import sys
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
args = vars(parser.parse_args())

try:
  client = messagebird.Client(args['accessKey'])

  webhookList = client.conversation_list_webhooks()

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