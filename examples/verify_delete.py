import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY   = ''
# VERIFY_ID = ''

try:
  ACCESS_KEY
except NameError:
  print('You need to set an ACCESS_KEY constant in this file')
  sys.exit(1)

try:
  VERIFY_ID
except NameError:
  print('You need to set a VERIFY_ID constant in this file')
  sys.exit(1)

try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Delete a Verification object.
  client.verify_delete(VERIFY_ID)    

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Verify object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
