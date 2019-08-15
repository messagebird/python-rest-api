import sys
import json
import io

from messagebird.balance import Balance
from messagebird.contact import Contact, ContactList
from messagebird.error import Error
from messagebird.group import Group, GroupList
from messagebird.hlr import HLR
from messagebird.message import Message, MessageList
from messagebird.mms import MMS
from messagebird.voicemessage import VoiceMessage
from messagebird.lookup import Lookup
from messagebird.verify import Verify
from messagebird.http_client import HttpClient, ResponseFormat
from messagebird.conversation_message import ConversationMessage, ConversationMessageList
from messagebird.conversation import Conversation, ConversationList
from messagebird.conversation_webhook import ConversationWebhook, ConversationWebhookList
from messagebird.voice_recording import VoiceRecordingsList, VoiceRecording

ENDPOINT = 'https://rest.messagebird.com'
CLIENT_VERSION = '1.4.1'
PYTHON_VERSION = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
USER_AGENT = 'MessageBird/ApiClient/%s Python/%s' % (CLIENT_VERSION, PYTHON_VERSION)
REST_TYPE = 'rest'

CONVERSATION_API_ROOT = 'https://conversations.messagebird.com/v1/'
CONVERSATION_PATH = 'conversations'
CONVERSATION_MESSAGES_PATH = 'messages'
CONVERSATION_WEB_HOOKS_PATH = 'webhooks'
CONVERSATION_TYPE = 'conversation'

VOICE_API_ROOT = 'https://voice.messagebird.com'
VOICE_PATH = 'calls'
VOICE_LEGS_PATH = 'legs'
VOICE_RECORDINGS_PATH = 'recordings'


class ErrorException(Exception):
    def __init__(self, errors):
        self.errors = errors
        message = ' '.join([str(e) for e in self.errors])
        super(ErrorException, self).__init__(message)


class Client(object):
    def __init__(self, access_key, http_client=None):
        self.access_key = access_key
        self.http_client = http_client

    def _get_http_client(self, type=REST_TYPE):
        if self.http_client:
            return self.http_client

        if type == REST_TYPE:
            return HttpClient(ENDPOINT, self.access_key, USER_AGENT)

        return HttpClient(CONVERSATION_API_ROOT, self.access_key, USER_AGENT)

    def request(self, path, method='GET', params=None, type=REST_TYPE):
        """Builds a request, gets a response and decodes it."""
        response_text = self._get_http_client(type).request(path, method, params)
        if not response_text:
            return response_text

        response_json = json.loads(response_text)

        if 'errors' in response_json:
            raise (ErrorException([Error().load(e) for e in response_json['errors']]))

        return response_json

    def request_plain_text(self, path, method='GET', params=None, type=REST_TYPE):
        """Builds a request, gets a response and returns the body."""
        response_text = self._get_http_client(type).request(path, method, params)

        try:
            # Try to decode the response to JSON to see if the API returned any
            # errors.
            response_json = json.loads(response_text)

            if 'errors' in response_json:
                raise (ErrorException([Error().load(e) for e in response_json['errors']]))
        except ValueError:
            # Do nothing: json.loads throws if the input string is not valid JSON,
            # which is expected. We'll just return the response body below.
            pass

        return response_text

    def request_store_as_file(self, path, filepath, method='GET', params=None, type=REST_TYPE):
        """Builds a request, gets a response and decodes it."""
        response_binary = self._get_http_client(type).request(path, method, params, ResponseFormat.binary)

        if not response_binary:
            return response_binary

        with io.open(filepath, 'wb') as f:
            f.write(response_binary)

        return filepath

    def balance(self):
        """Retrieve your balance."""
        return Balance().load(self.request('balance'))

    def hlr(self, id):
        """Retrieve the information of a specific HLR lookup."""
        return HLR().load(self.request('hlr/' + str(id)))

    def hlr_create(self, msisdn, reference):
        """Perform a new HLR lookup."""
        return HLR().load(self.request('hlr', 'POST', {'msisdn': msisdn, 'reference': reference}))

    def message(self, id):
        """Retrieve the information of a specific message."""
        return Message().load(self.request('messages/' + str(id)))

    def message_list(self, limit=20, offset=0):
        """Retrieve a list of the most recent messages."""
        query = 'limit=' + str(limit) + '&offset=' + str(offset)
        return MessageList().load(self.request('messages?' + query))

    def message_create(self, originator, recipients, body, params=None):
        """Create a new message."""
        if params is None: params = {}
        if type(recipients) == list:
            recipients = ','.join(recipients)

        params.update({'originator': originator, 'body': body, 'recipients': recipients})
        return Message().load(self.request('messages', 'POST', params))

    def message_delete(self, id):
        """Delete a message from the dashboard."""
        self.request_plain_text('messages/' + str(id), 'DELETE')

    def mms_create(self, originator, recipients, body, mediaUrls, subject = None, reference = None, scheduledDatetime = None):
        ''' Send bulk mms.

        Args:
            originator(str): name of the originator
            recipients(str/list(str)): comma seperated numbers or list of numbers in E164 format
            body(str)       : text message body
            mediaUrl(str)   : list of URL's of attachments of the MMS message.
            subject(str)    : utf-encoded subject
            reference(str)  : client reference text
            scheduledDatetime(str) : scheduled date time in RFC3339 format
        Raises:
            ErrorException:  On api returning errors

        Returns:
            MMS: On success an MMS instance instantiated with succcess response
        '''
        if isinstance(recipients,list):
            recipients = ','.join(recipients)
        if isinstance(mediaUrls,str):
            mediaUrls = [mediaUrls]
        params = locals()
        del(params['self'])
        return  MMS().load(self.request('mms', 'POST', params))

    def voice_message(self, id):
        "Retrieve the information of a specific voice message."
        return VoiceMessage().load(self.request('voicemessages/' + str(id)))

    def voice_message_create(self, recipients, body, params=None):
        """Create a new voice message."""
        if params is None: params = {}
        if type(recipients) == list:
            recipients = ','.join(recipients)

        params.update({'recipients': recipients, 'body': body})
        return VoiceMessage().load(self.request('voicemessages', 'POST', params))

    def lookup(self, phonenumber, params=None):
        """Do a new lookup."""
        if params is None: params = {}
        return Lookup().load(self.request('lookup/' + str(phonenumber), 'GET', params))

    def lookup_hlr(self, phonenumber, params=None):
        """Retrieve the information of a specific HLR lookup."""
        if params is None: params = {}
        return HLR().load(self.request('lookup/' + str(phonenumber) + '/hlr', 'GET', params))

    def lookup_hlr_create(self, phonenumber, params=None):
        """Perform a new HLR lookup."""
        if params is None: params = {}
        return HLR().load(self.request('lookup/' + str(phonenumber) + '/hlr', 'POST', params))

    def verify(self, id):
        """Retrieve the information of a specific verification."""
        return Verify().load(self.request('verify/' + str(id)))

    def verify_create(self, recipient, params=None):
        """Create a new verification."""
        if params is None: params = {}
        params.update({'recipient': recipient})
        return Verify().load(self.request('verify', 'POST', params))

    def verify_verify(self, id, token):
        """Verify the token of a specific verification."""
        return Verify().load(self.request('verify/' + str(id), params={'token': token}))

    def verify_delete(self, id):
        """Delete an existing verification object."""
        self.request_plain_text('verify/' + str(id), 'DELETE')

    def contact(self, id):
        """Retrieve the information of a specific contact."""
        return Contact().load(self.request('contacts/' + str(id)))

    def contact_create(self, phonenumber, params=None):
        if params is None: params = {}
        params.update({'msisdn': phonenumber})
        return Contact().load(self.request('contacts', 'POST', params))

    def contact_delete(self, id):
        self.request_plain_text('contacts/' + str(id), 'DELETE')

    def contact_update(self, id, params=None):
        self.request_plain_text('contacts/' + str(id), 'PATCH', params)

    def contact_list(self, limit=10, offset=0):
        query = self._format_query(limit, offset)
        return ContactList().load(self.request('contacts?' + query, 'GET', None))

    def group(self, id):
        return Group().load(self.request('groups/' + str(id), 'GET', None))

    def group_create(self, name, params=None):
        if params is None: params = {}
        params.update({'name': name})
        return Group().load(self.request('groups', 'POST', params))

    def group_delete(self, id):
        self.request_plain_text('groups/' + str(id), 'DELETE', None)

    def group_list(self, limit=10, offset=0):
        query = self._format_query(limit, offset)
        return GroupList().load(self.request('groups?' + query, 'GET', None))

    def group_update(self, id, name, params=None):
        if params is None: params = {}
        params.update({'name': name})
        self.request_plain_text('groups/' + str(id), 'PATCH', params)

    def group_add_contacts(self, groupId, contactIds):
        query = self.__group_add_contacts_query(contactIds)
        self.request_plain_text('groups/' + str(groupId) + '?' + query, 'PUT', None)

    def __group_add_contacts_query(self, contactIds):
        # __group_add_contacts_query gets a query string to add contacts to a
        # group. The expected format is ids[]=first-contact&ids[]=second-contact.
        # See: https://developers.messagebird.com/docs/groups#add-contact-to-group.
        return '&'.join('ids[]=' + str(id) for id in contactIds)

    def group_remove_contact(self, groupId, contactId):
        self.request_plain_text('groups/' + str(groupId) + '/contacts/' + str(contactId), 'DELETE', None)

    def conversation_list(self, limit=10, offset=0):
        uri = CONVERSATION_PATH + '?' + self._format_query(limit, offset)
        return ConversationList().load(self.request(uri, 'GET', None, CONVERSATION_TYPE))

    def conversation_start(self, start_request):
        uri = CONVERSATION_PATH + '/start'
        return Conversation().load(self.request(uri, 'POST', start_request, CONVERSATION_TYPE))

    def conversation_update(self, id, update_request):
        uri = CONVERSATION_PATH + '/' + str(id)
        return Conversation().load(self.request(uri, 'PATCH', update_request, CONVERSATION_TYPE))

    def conversation_read(self, id):
        uri = CONVERSATION_PATH + '/' + str(id)
        return Conversation().load(self.request(uri, 'GET', None, CONVERSATION_TYPE))

    def conversation_list_messages(self, conversation_id, limit=10, offset=0):
        uri = CONVERSATION_PATH + '/' + str(conversation_id) + '/' + CONVERSATION_MESSAGES_PATH
        uri += '?' + self._format_query(limit, offset)

        return ConversationMessageList().load(self.request(uri, 'GET', None, CONVERSATION_TYPE))

    def conversation_create_message(self, conversation_id, message_create_request):
        uri = CONVERSATION_PATH + '/' + str(conversation_id) + '/' + CONVERSATION_MESSAGES_PATH
        return ConversationMessage().load(self.request(uri, 'POST', message_create_request, CONVERSATION_TYPE))

    def conversation_read_message(self, message_id):
        uri = CONVERSATION_MESSAGES_PATH + '/' + str(message_id)
        return ConversationMessage().load(self.request(uri, 'GET', None, CONVERSATION_TYPE))

    def conversation_create_webhook(self, webhook_create_request):
        return ConversationWebhook().load(
            self.request(CONVERSATION_WEB_HOOKS_PATH, 'POST', webhook_create_request, CONVERSATION_TYPE))

    def conversation_update_webhook(self, id, update_request):
        """
        Updates a webhook with the supplied parameters.

        API Reference: https://developers.messagebird.com/api/conversations/#webhooks
        """
        uri = CONVERSATION_WEB_HOOKS_PATH + '/' + str(id)
        web_hook = self.request(uri, 'PATCH', update_request, CONVERSATION_TYPE)
        return ConversationWebhook().load(web_hook)

    def conversation_delete_webhook(self, id):
        uri = CONVERSATION_WEB_HOOKS_PATH + '/' + str(id)
        self.request(uri, 'DELETE', None, CONVERSATION_TYPE)

    def conversation_list_webhooks(self, limit=10, offset=0):
        uri = CONVERSATION_WEB_HOOKS_PATH + '?' + self._format_query(limit, offset)

        return ConversationWebhookList().load(self.request(uri, 'GET', None, CONVERSATION_TYPE))

    def conversation_read_webhook(self, id):
        uri = CONVERSATION_WEB_HOOKS_PATH + '/' + str(id)
        return ConversationWebhook().load(self.request(uri, 'GET', None, CONVERSATION_TYPE))

    def voice_recording_list_recordings(self, call_id, leg_id):
        uri = VOICE_API_ROOT + '/' + VOICE_PATH + '/' + str(call_id) + '/' + VOICE_LEGS_PATH + '/' + str(leg_id) + '/' + VOICE_RECORDINGS_PATH
        return VoiceRecordingsList().load(self.request(uri, 'GET'))

    def voice_recording_view(self, call_id, leg_id, recording_id):
        uri = VOICE_API_ROOT + '/' + VOICE_PATH + '/' + str(call_id) + '/' + VOICE_LEGS_PATH + '/' + str(leg_id) + '/' + VOICE_RECORDINGS_PATH + '/' + str(recording_id)
        recording_response = self.request(uri, 'GET')
        recording_links = recording_response.get('_links')
        if recording_links is not None:
            recording_response['data'][0]['_links'] = recording_links
        return VoiceRecording().load(recording_response['data'][0])

    def voice_recording_download(self, call_id, leg_id, recording_id):
        uri = VOICE_API_ROOT + '/' + VOICE_PATH + '/' + str(call_id) + '/' + VOICE_LEGS_PATH + '/' + str(leg_id) + '/' + VOICE_RECORDINGS_PATH + '/' + str(recording_id)
        recording_response = self.request(uri, 'GET')
        recording_links = recording_response.get('_links')
        if recording_links is None or recording_links.get('file') is None:
            raise (ErrorException('There is no recording available'))
        recording_file = recording_links.get('file')
        recording_file = self.request_store_as_file(VOICE_API_ROOT + recording_file, recording_id + '.wav')
        return VOICE_API_ROOT + recording_file

    def _format_query(self, limit, offset):
        return 'limit=' + str(limit) + '&offset=' + str(offset)
