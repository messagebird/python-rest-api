#!/usr/bin/env python
import sys
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--conversationId', help='conversation that you want the list of messages', type=str, required=True)
args = vars(parser.parse_args())

try:
  client = messagebird.Client(args['accessKey'])

  msg = client.conversation_list_messages(args['conversationId'])

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
