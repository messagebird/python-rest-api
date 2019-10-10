#!/usr/bin/env python
import argparse
import messagebird
from messagebird.voice_webhook import VoiceUpdateWebhookRequest

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--webhookId', help='webhook that you want to update', type=str, required=True)
parser.add_argument('--title', help='title for the webhook', type=str)
parser.add_argument('--token', help='token for the webhook', type=str)

args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    update_webhook_request = VoiceUpdateWebhookRequest(title=args['title'], token=args['token'])
    webhook = client.voice_update_webhook(args['webhookId'], update_webhook_request)

    # Print the object information.
    print('\nThe following information was returned as a Voice Webhook object:\n')
    print('  id                 : {}'.format(webhook.id))
    print('  token              : {}'.format(webhook.token))
    print('  url                : {}'.format(webhook.url))
    print('  createdAtDatetime  : {}'.format(webhook.createdDatetime))
    print('  updatedAtDatetime  : {}'.format(webhook.updatedDatetime))

except messagebird.client.ErrorException as e:
    print('An error occured while updating a Voice Webhook object:')

    for error in e.errors:
        print('  code        : {}'.format(error.code))
        print('  description : {}'.format(error.description))
        print('  parameter   : {}\n'.format(error.parameter))



