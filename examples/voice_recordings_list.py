#!/usr/bin/env python
import messagebird
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--callID', help='identifier for the call', type=str, required=True)
parser.add_argument('--legID', help='identifier for the leg object you wish to list the recordings for', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    voiceRecordingList = client.voice_recording_list_recordings(args['callID'], args['legID'])

    # Print the object information.
    print('The following information was returned as a Voice Recordings List object:')
    print(voiceRecordingList)

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Message object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
