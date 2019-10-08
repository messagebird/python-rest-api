#!/usr/bin/env python
import argparse
import messagebird
from messagebird.voice_webhook import VoiceCreateWebhookRequest

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)

args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    webhooks_list = client.voice_list_webhooks(limit=5, offset=0)

    if webhooks_list is None or webhooks_list.data is None:
        print("\nNo webhooks\n")
        exit(0)
    # Print the object information.
    print('\nThe following information was returned as a Voice Webhook objects:\n')
    for webhook in webhooks_list.data:
        print('{')
        print('  id                 : %s' % webhook.id)
        print('  token              : %s' % webhook.token)
        print('  url                : %s' % webhook.url)
        print('  createdAtDatetime  : %s' % webhook.createdDatetime)
        print('  updatedAtDatetime  : %s' % webhook.updatedDatetime)
        print('}\n')

except messagebird.client.ErrorException as e:
    print('An error occured while reading a Voice Webhook object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
