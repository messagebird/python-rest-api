#!/usr/bin/env python
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--webhookId', help='webhook that you want to update', type=str, required=True)

args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])
    webhook = client.voice_delete_webhook(args['webhookId'])

    # Print the object information.
    print('Webhook has been deleted')

except messagebird.client.ErrorException as e:
    print('An error occured while deleting a Voice Webhook object:')

    for error in e.errors:
        print('  code        : {}'.format(error.code))
        print('  description : {}'.format(error.description))
        print('  parameter   : {}\n'.format(error.parameter))
