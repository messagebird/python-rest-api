#!/usr/bin/env python
import messagebird
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    conversationList = client.conversation_list()

    # Print the object information.
    print('The following information was returned as a Conversation List object:')
    print(conversationList)

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Message object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
