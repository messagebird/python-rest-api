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
    print('  id           : {}'.format(call.id))
    print('  steps        : ')
    for step in call.steps:
        print(step)

    print('  record       : {}'.format(call.record))
    print('  default      : {}'.format(call.default))
    print('  updatedAt    : {}'.format(call.updatedAt))
    print('  createdAt    : {}'.format(call.createdAt))

except messagebird.client.ErrorException as e:
    print('\nAn error occured while requesting a CallFlow object:\n')

    for error in e.errors:
        print('  code        : {}'.format(error.code))
        print('  description : {}'.format(error.description))
        print('  parameter   : {}\n'.format(error.parameter))
