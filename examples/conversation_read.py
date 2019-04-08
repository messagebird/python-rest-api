#!/usr/bin/env python
import messagebird
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--conversationId', help='conversation that you want the message list', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    conversation = client.conversation_read(args['conversationId'])

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
