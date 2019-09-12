#!/usr/bin/env python
import argparse
from messagebird import client, Client

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--callID', help='identifier for the call', type=str, required=True)
parser.add_argument('--legID', help='identifier for the leg object you wish to list the recordings for', type=str, required=True)
parser.add_argument('--recordingID', help='identifier for the recording', type=str, required=True)
parser.add_argument('--transcriptionFile', help='identifier for the transcription file', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = Client(args['accessKey'])
    client.voice_transcription_download(
        args['callID'],
        args['legID'],
        args['recordingID'],
        args['transcriptionFile']
    )

except client.ErrorException as e:
    print('An error occured while requesting a Voice Transcriptions object list object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
