#!/usr/bin/env python
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--webhookId', help='webhook that you want to delete', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    client.conversation_delete_webhook(args['webhookId'])

    # Print the object information.
    print('\nWebhook has been deleted:\n')

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a Webhook object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
