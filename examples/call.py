#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY = ''
# CALL_ID = ''

try:
    ACCESS_KEY
except NameError:
    print('You need to set an ACCESS_KEY constant in this file')
    sys.exit(1)

try:
    CALL_ID
except NameError:
    print('You need to set a CALL_ID constant in this file')
    sys.exit(1)

try:
    # Create a MessageBird client with the specified ACCESS_KEY.
    client = messagebird.Client(ACCESS_KEY)

    # Fetch the Call object for the specified CALL_ID.
    call = client.call(CALL_ID)

    # Print the object information.
    print('\nThe following information was returned as a', str(call.__class__), 'object:\n')
    print('  '.join(str(call).splitlines(True)))

except messagebird.client.ErrorException as e:
    print('\nAn error occurred while requesting a Message object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
