#!/usr/bin/env python
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    webhook_list = client.conversation_list_webhooks()

    # Print the object information.
    print('The following information was returned as a Conversation Webhook List object:')
    print(webhook_list)

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a Conversation Webhook List object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
