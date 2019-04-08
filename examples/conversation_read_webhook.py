#!/usr/bin/env python
import messagebird
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--webhookId', help='webhook that you want to read', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    webhook = client.conversation_read_webhook(args['webhookId'])

    # Print the object information.
    print('\nThe following information was returned as a Webhook object:\n')
    print('  id            : %s' % webhook.id)
    print('  events        : %s' % webhook.events)
    print('  channel id    : %s' % webhook.channelId)
    print('  created date  : %s' % webhook.createdDatetime)
    print('  updated date  : %s' % webhook.updatedDatetime)

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a Webhook object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
