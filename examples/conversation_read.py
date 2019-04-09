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
    print('The following information was returned as a Conversation object:')
    print(conversation)

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a Conversation object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
