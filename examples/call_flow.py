#!/usr/bin/env python

import sys
import messagebird

#ACCESS_KEY = ''
#CALL_FLOW_ID = ''

try:
    ACCESS_KEY
except NameError:
    print('You need to set an ACCESS_KEY constant in this file')
    sys.exit(1)

try:
    CALL_FLOW_ID
except NameError:
    print('You need to set a CALL_FLOW_ID constant in this file')
    sys.exit(1)

try:
    # Create a MessageBird client with the specified ACCESS_KEY.
    client = messagebird.Client(ACCESS_KEY)

    # Fetch the CallFlow object for the specified CALL_FLOW_ID.
    call = client.call_flow(CALL_FLOW_ID)

    # Print the object information.
    print('\nThe following information was returned as a CallFlow object:\n')
    print('  id           : %s' % call.id)
    print('  title        : %s' % call.title)
    print('  steps        : ')
    for step in call.steps:
        print(step)

    print('  record       : %s' % call.record)
    print('  default      : %s' % call.default)
    print('  updatedAt    : %s' % call.updatedAt)
    print('  createdAt    : %s' % call.createdAt)

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a CallFlow object:\n')

    for error in e.errors:
        print('  code        : %d' % error.code)
        print('  description : %s' % error.description)
        print('  parameter   : %s\n' % error.parameter)
