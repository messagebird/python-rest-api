#!/usr/bin/env python
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--messageId', help='message that you want to read', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    msg = client.conversation_read_message(args['messageId'])

    # Print the object information.
    print('\nThe following information was returned as a Conversation List object:\n')
    print('  message id   : %s' % msg.id)
    print('  channel id   : %s' % msg.channelId)
    print('  direction    : %s' % msg.direction)
    print('  content      : %s' % msg.content)
    print('  content      : %s' % msg.content)
    print('  status       : %s' % msg.status)
    print('  type         : %s' % msg.type)
    print('  created date : %s' % msg.createdDatetime)
    print('  updated date : %s' % msg.updatedDatetime)

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a Message object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
