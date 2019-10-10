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
        print('  id                 : {}'.format(webhook.id))
        print('  token              : {}'.format(webhook.token))
        print('  url                : {}'.format(webhook.url))
        print('  createdAtDatetime  : {}'.format(webhook.createdDatetime))
        print('  updatedAtDatetime  : {}'.format(webhook.updatedDatetime))
        print('}\n')

except messagebird.client.ErrorException as e:
    print('An error occured while reading a Voice Webhook object:')

    for error in e.errors:
        print('  code        : {}'.format(error.code))
        print('  description : {}'.format(error.description))
        print('  parameter   : {}\n'.format(error.parameter))
