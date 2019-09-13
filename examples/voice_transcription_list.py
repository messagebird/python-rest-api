#!/usr/bin/env python
import argparse
import messagebird

parser = argparse.ArgumentParser()
parser.add_argument('--accessKey', help='access key for MessageBird API', type=str, required=True)
parser.add_argument('--callID', help='identifier for the call', type=str, required=True)
parser.add_argument('--legID', help='identifier for the leg object you wish to list the recordings for', type=str, required=True)
parser.add_argument('--recordingID', help='identifier for the recording', type=str, required=True)
args = vars(parser.parse_args())

try:
    client = messagebird.Client(args['accessKey'])

    voiceTranscriptions = client.voice_transcription_list(
        args['callID'],
        args['legID'],
        args['recordingID']
    )

    print('\nThe following information was returned as a %s object:\n' % voiceTranscriptions.__class__)
    if voiceTranscriptions.items is not None:
        print('  Containing the the following items:')
        for item in voiceTranscriptions.items:
            print('  {')
            print('    id                : %s' % item.id)
            print('    recording id      : %s' % item.recordingId)
            print('    leg id            : %s' % item.legId)
            print('    status            : %s' % item.status)
            print('    createdAt         : %s' % item.createdAt)
            print('    updatedAt         : %s' % item.updatedAt)
            print('  },')
    else:
        print('  With an empty response.')

except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Voice Transcriptions object list object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
