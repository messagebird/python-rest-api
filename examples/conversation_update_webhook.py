#!/usr/bin/env python
import messagebird
import argparse
from messagebird.conversation_webhook import \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED, \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED


parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--webhookId', help='webhook that you want to update', type=str, required=True)
parser.add_argument('--url', help='url for the webhook', type=str)
parser.add_argument('--status', help='Status of the webhook. Can be set to "enabled" or "disabled"', type=str, default='enabled')
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    update_request = {
        'events': [CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED, CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED],
        'url': args['url'],
        'status': args['status']
    }
    webhook = client.conversation_update_webhook(args['webhookId'], update_request)

    # Print the object information.
    print('The following information was returned as a Webhook object:')
    print(webhook)

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Webhook object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
