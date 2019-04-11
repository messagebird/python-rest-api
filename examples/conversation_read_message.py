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
    print('The following information was returned as a Conversation List object:')
    print(msg)

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Message object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
