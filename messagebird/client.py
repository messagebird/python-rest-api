import sys
import json
import requests

try:
  from urllib.parse import urljoin
except ImportError:
  from urlparse import urljoin

from messagebird.base         import Base
from messagebird.balance      import Balance
from messagebird.error        import Error
from messagebird.hlr          import HLR
from messagebird.message      import Message
from messagebird.voicemessage import VoiceMessage
from messagebird.lookup       import Lookup
from messagebird.verify       import Verify

ENDPOINT       = 'https://rest.messagebird.com'
CLIENT_VERSION = '1.2.1'
PYTHON_VERSION = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])


class ErrorException(Exception):
  def __init__(self, errors):
    self.errors = errors
    message = ' '.join([str(e) for e in self.errors])
    super(ErrorException, self).__init__(message)


class Client(object):
  def __init__(self, access_key):
    self.access_key = access_key
    self._supported_status_codes = [200, 201, 204, 401, 404, 405, 422]

  def request(self, path, method='GET', params=None, timeout=None):
    if params is None: params = {}
    url = urljoin(ENDPOINT, path)

    headers = {
      'Accept'        : 'application/json',
      'Authorization' : 'AccessKey ' + self.access_key,
      'User-Agent'    : 'MessageBird/ApiClient/%s Python/%s' % (CLIENT_VERSION, PYTHON_VERSION),
      'Content-Type'  : 'application/json'
    }

    if method == 'GET':
      response = requests.get(url, verify=True, headers=headers, params=params, timeout=timeout)
    else:
      response = requests.post(url, verify=True, headers=headers, data=json.dumps(params), timeout=timeout)

    if response.status_code in self._supported_status_codes:
      json_response = response.json()
    else:
      response.raise_for_status()

    if 'errors' in json_response:
      raise(ErrorException([Error().load(e) for e in json_response['errors']]))

    return json_response

  def balance(self, timeout=None):
    """Retrieve your balance."""
    return Balance().load(self.request('balance', timeout=timeout))

  def hlr(self, id):
    """Retrieve the information of a specific HLR lookup."""
    return HLR().load(self.request('hlr/' + str(id), timeout=timeout))

  def hlr_create(self, msisdn, reference, timeout=None):
    """Perform a new HLR lookup."""
    return HLR().load(self.request('hlr', 'POST', { 'msisdn' : msisdn, 'reference' : reference }, timeout=timeout))

  def message(self, id, timeout=None):
    """Retrieve the information of a specific message."""
    return Message().load(self.request('messages/' + str(id), timeout=timeout))

  def message_create(self, originator, recipients, body, params=None, timeout=None):
    """Create a new message."""
    if params is None: params = {}
    if type(recipients) == list:
      recipients = ','.join(recipients)

    params.update({ 'originator' : originator, 'body' : body, 'recipients' : recipients })
    return Message().load(self.request('messages', 'POST', params, timeout=timeout))

  def voice_message(self, id, timeout=None):
    "Retrieve the information of a specific voice message."
    return VoiceMessage().load(self.request('voicemessages/' + str(id), timeout=timeout))

  def voice_message_create(self, recipients, body, params=None, timeout=None):
    """Create a new voice message."""
    if params is None: params = {}
    if type(recipients) == list:
      recipients = ','.join(recipients)

    params.update({ 'recipients' : recipients, 'body' : body })
    return VoiceMessage().load(self.request('voicemessages', 'POST', params, timeout=timeout))

  def lookup(self, phonenumber, params=None, timeout=None):
    """Do a new lookup."""
    if params is None: params = {}
    return Lookup().load(self.request('lookup/' + str(phonenumber), 'GET', params, timeout=timeout))

  def lookup_hlr(self, phonenumber, params=None, timeout=None):
    """Retrieve the information of a specific HLR lookup."""
    if params is None: params = {}
    return HLR().load(self.request('lookup/' + str(phonenumber) + '/hlr', 'GET', params, timeout=timeout))

  def lookup_hlr_create(self, phonenumber, params=None, timeout=None):
    """Perform a new HLR lookup."""
    if params is None: params = {}
    return HLR().load(self.request('lookup/' + str(phonenumber) + '/hlr', 'POST', params, timeout=timeout))

  def verify(self, id, timeout=None):
    """Retrieve the information of a specific verification."""
    return Verify().load(self.request('verify/' + str(id), timeout=timeout))

  def verify_create(self, recipient, params=None, timeout=None):
    """Create a new verification."""
    if params is None: params = {}
    params.update({ 'recipient' : recipient })
    return Verify().load(self.request('verify', 'POST', params, timeout=timeout))

  def verify_verify(self, id, token, timeout=None):
    """Verify the token of a specific verification."""
    return Verify().load(self.request('verify/' + str(id), params={'token': token}, timeout=timeout))
