#!/usr/bin/env python
import messagebird
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
args = vars(parser.parse_args())

try:
  client = messagebird.Client(args['accessKey'])

  conversationList = client.conversation_list()

  itemIds = []
  for msgItem in conversationList.items:
    itemIds.append(msgItem.id)

  # Print the object information.
  print('\nThe following information was returned as a Conversation List object:\n')
  print('  conversation ids  : %s' % itemIds)
  print('  offset       : %s' % conversationList.offset)
  print('  limit        : %s' % conversationList.limit)
  print('  totalCount   : %s' % conversationList.totalCount)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Message object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
