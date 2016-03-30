import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import messagebird

# ACCESS_KEY   = ''
# VERIFY_ID    = ''
# VERIFY_TOKEN = ''

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
  VERIFY_TOKEN
except NameError:
  print('You need to set a VERIFY_TOKEN constant in this file')
  sys.exit(1)


try:
  # Create a MessageBird client with the specified ACCESS_KEY.
  client = messagebird.Client(ACCESS_KEY)

  # Create a new Lookup HLR object.
  verify = client.verify_verify(VERIFY_ID, VERIFY_TOKEN)

  # Print the object information.
  print('\nThe following information was returned as a Verify object:\n')
  print('  id                  : %s' % verify.id)
  print('  href                : %s' % verify.href)
  print('  recipient           : %s' % verify.recipient)
  print('  reference           : %s' % verify.reference)
  print('  messages            : %s' % verify.messages)
  print('  status              : %s' % verify.status)
  print('  createdDatetime     : %s' % verify.createdDatetime)
  print('  validUntilDatetime  : %s\n' % verify.validUntilDatetime)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Verify object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)
