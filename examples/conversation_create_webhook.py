#!/usr/bin/env python
import argparse
import messagebird
from messagebird.conversation_webhook import \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED, \
    CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--channelId', help='channel that you want create the webhook', type=str, required=True)
parser.add_argument('--url', help='url for the webhook', type=str)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    webhook = client.conversation_create_webhook({
        'channelId': args['channelId'],
        'events': [CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED, CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED],
        'url': args['url']
    })

    # Print the object information.
    print('The following information was returned as a Webhook object:')
    print(webhook)

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Webhook object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
