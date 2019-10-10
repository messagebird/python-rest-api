#!/usr/bin/env python
import argparse
import messagebird
from messagebird.voice_webhook import VoiceCreateWebhookRequest

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--webhookId', help='webhook that you want to update', type=str, required=True)

args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    webhook = client.voice_read_webhook(args['webhookId'])

    # Print the object information.
    print('\nThe following information was returned as a Voice Webhook object:\n')

    print('  id                 : {}'.format(webhook.id))
    print('  token              : {}'.format(webhook.token))
    print('  url                : {}'.format(webhook.url))
    print('  createdAtDatetime  : {}'.format(webhook.createdDatetime))
    print('  updatedAtDatetime  : {}'.format(webhook.updatedDatetime))


except messagebird.client.ErrorException as e:
    print('An error occured while reading a Voice Webhook object:')

    for error in e.errors:
        print('  code        : {}'.format(error.code))
        print('  description : {}'.format(error.description))
        print('  parameter   : {}\n'.format(error.parameter))
