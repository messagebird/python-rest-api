#!/usr/bin/env python
import argparse
import messagebird
from messagebird.conversation_message import MESSAGE_TYPE_TEXT

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--channelId', help='channel that you want to start a conversation', type=str, required=True)
parser.add_argument('--phoneNumber', help='phone number that you want to send a message', type=str, required=True)
parser.add_argument('--textMessage', help='text that you want to send', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    msg = client.conversation_start(
        {'channelId': args['channelId'], 'to': args['phoneNumber'], 'type': MESSAGE_TYPE_TEXT,
         'content': {'text': args['textMessage']}})

    # Print the object information.
    print('The following information was returned as a Conversation object:')
    print(msg)

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Message object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
