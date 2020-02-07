#!/usr/bin/env python

import messagebird
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# ACCESS_KEY = ''

try:
    # Create a MessageBird client with the specified ACCESS_KEY.
    client = messagebird.Client(ACCESS_KEY)

    # Fetch Voice Messages List from a specific offset, and within a defined limit.
    voiceMessageList = client.voice_message_list(limit=10, offset=0)

    # Print the object information.
    print('The following information was returned as a Voice Messages List object:')
    print('  Containing the following items:')
    print(voiceMessageList)
    for item in voiceMessageList.items:
        print('  {')
        print('  id                : %s' % item.id)
        print('  href              : %s' % item.href)
        print('  originator        : %s' % item.originator)
        print('  body              : %s' % item.body)
        print('  reference         : %s' % item.reference)
        print('  language          : %s' % item.language)
        print('  voice             : %s' % item.voice)
        print('  repeat            : %s' % item.repeat)
        print('  ifMachine         : %s' % item.ifMachine)
        print('  scheduledDatetime : %s' % item.scheduledDatetime)
        print('  createdDatetime   : %s' % item.createdDatetime)
        print('  recipients        : %s\n' % item.recipients)
        print('  },')


except messagebird.client.ErrorException as e:
    print('An error occured while requesting a Voice messages object list object:')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
