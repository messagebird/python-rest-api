#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

ACCESS_KEY = os.environ.get('ACCESS_KEY', None)
if ACCESS_KEY is None:
  print("Set environment ACCESS_KEY  from https://dashboard.messagebird.com/en/developers/access")
  exit(1)

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)
  # Send a MMS 
  mms = client.mms_create('Sarath','+4915238456487','Rich test message','https://www.messagebird.com/assets/images/og/messagebird.gif')
  # Print the object information.
  print("The following information was returned as a MMS object:\n%s" % mms)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting to send a MMS:\n')
  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)