import sys
import json
import io

from messagebird.balance import Balance
from messagebird.call import Call
from messagebird.call_list import CallList
from messagebird.contact import Contact, ContactList
from messagebird.error import Error, ValidationError
from messagebird.group import Group, GroupList
from messagebird.hlr import HLR
from messagebird.message import Message, MessageList
from messagebird.mms import MMS
from messagebird.voice_webhook import VoiceWebhook, VoiceWebhookList
from messagebird.voicemessage import VoiceMessagesList, VoiceMessage
from messagebird.lookup import Lookup
from messagebird.verify import Verify
from messagebird.http_client import HttpClient, ResponseFormat
from messagebird.conversation_message import ConversationMessage, ConversationMessageList
from messagebird.conversation import Conversation, ConversationList
from messagebird.conversation_webhook import ConversationWebhook, ConversationWebhookList
from messagebird.voice_recording import VoiceRecordingsList, VoiceRecording
from messagebird.voice_transcription import VoiceTranscriptionsList, VoiceTranscriptionsView
from messagebird.call_flow import CallFlow, CallFlowList, CallFlowNumberList
from messagebird.number import Number, NumberList
from messagebird.version import VERSION

ENDPOINT = 'https://rest.messagebird.com'
PYTHON_VERSION = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
USER_AGENT = 'MessageBird/ApiClient/%s Python/%s' % (VERSION, PYTHON_VERSION)
REST_TYPE = 'rest'

CONVERSATION_API_ROOT = 'https://conversations.messagebird.com/v1/'
CONVERSATION_PATH = 'conversations'
CONVERSATION_MESSAGES_PATH = 'messages'
CONVERSATION_WEB_HOOKS_PATH = 'webhooks'
CONVERSATION_TYPE = 'conversation'

VOICE_API_ROOT = 'https://voice.messagebird.com'
VOICE_TYPE = 'voice'
VOICE_PATH = 'calls'
VOICE_LEGS_PATH = 'legs'
VOICE_RECORDINGS_PATH = 'recordings'
VOICE_TRANSCRIPTIONS_PATH = 'transcriptions'
VOICE_WEB_HOOKS_PATH = 'webhooks'

NUMBER_TYPE = 'number'
NUMBER_API_ROOT = 'https://numbers.messagebird.com/v1/'
NUMBER_PATH = 'phone-numbers'
NUMBER_AVAILABLE_PATH = 'available-phone-numbers'


class ErrorException(Exception):
    def __init__(self, errors):
        self.errors = errors
        message = ' '.join([str(e) for e in self.errors])
        super(ErrorException, self).__init__(message)


class SignleErrorException(Exception):
    def __init__(self, errorMessage):
        super(SignleErrorException, self).__init__(errorMessage)


class Client(object):
    def __init__(self, access_key, http_client=None):
        self.access_key = access_key
        self.http_client = http_client

    def _get_http_client(self, type=REST_TYPE):
        if self.http_client:
            return self.http_client

        if type == CONVERSATION_TYPE:
            return HttpClient(CONVERSATION_API_ROOT, self.access_key, USER_AGENT)

        if type == VOICE_TYPE:
            return HttpClient(VOICE_API_ROOT, self.access_key, USER_AGENT)

        if type == NUMBER_TYPE:
            return HttpClient(NUMBER_API_ROOT, self.access_key, USER_AGENT)

        return HttpClient(ENDPOINT, self.access_key, USER_AGENT)

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

    def call(self, id):
        """Retrieve the information of a specific call"""
        return Call().load(self.request('calls/' + str(id), 'GET', None, VOICE_TYPE))

    def call_list(self, page=1):
        """Listing calls

        Args:
            page(int)               : The page to list.
        Raises:
            ErrorException          : On api returning errors

        Returns:
            CallList(object)        : The list of calls requested & their status."""
        return CallList().load(self.request('calls/?page=' + str(page), 'GET', None, VOICE_TYPE))

    def call_create(self, source, destination, callFlow, webhook):
        """Creating a call

        Args:
            source(str)             : The caller ID of the call.
            destination(string)     : The number/address to be called.
            callFlow(object)        : The call flow object to be executed when the call is answered.
            webhook(object)         : The webhook object containing the url & required token.
        Raises:
            ErrorException          : On api returning errors

        Returns:
            Call(object)            : The Call object just created."""

        params = locals()
        del (params['self'])
        return Call().load(self.request('calls/', 'POST', params, VOICE_TYPE))

    def call_delete(self, id):
        """Delete an existing call object."""
        response = self.request_plain_text('calls/' + str(id), 'DELETE', None, VOICE_TYPE)

        # successful delete should be empty
        if len(response) > 0:
            raise SignleErrorException(response)

    def hlr(self, id):
        """Retrieve the information of a specific HLR lookup."""
        return HLR().load(self.request('hlr/' + str(id)))

    def hlr_create(self, msisdn, reference):
        """Perform a new HLR lookup."""
        return HLR().load(self.request('hlr', 'POST', {'msisdn': msisdn, 'reference': reference}))

    def message(self, id):
        """Retrieve the information of a specific message."""
        return Message().load(self.request('messages/' + str(id)))

    def message_list(self, limit=20, offset=0, status=None):
        """Retrieve a list of the most recent messages.

        Args:
            limit(int)                     : The page limit.
            offset(int)                    : The page to list.
            status(str)                    : Message status filter(scheduled, sent, buffered, delivered, expired or delivery_failed)
        Returns:
            MessageList(object)            : The List of the message requested."""
        query = self._format_query(limit, offset)
        if status:
            query = query + "&status=" + status
        return MessageList().load(self.request('messages?' + query))

    def message_create(self, originator, recipients, body, params=None):
        """Create a new message."""
        if params is None:
            params = {}
        if type(recipients) == list:
            recipients = ','.join(recipients)

        params.update({'originator': originator, 'body': body, 'recipients': recipients})
        return Message().load(self.request('messages', 'POST', params))

    def message_delete(self, id):
        """Delete a message from the dashboard."""
        self.request_plain_text('messages/' + str(id), 'DELETE')

    def mms_create(self, originator, recipients, body, mediaUrls, subject=None, reference=None, scheduledDatetime=None):
        """ Send bulk mms.

        Args:
            originator(str): name of the originator
            recipients(str/list(str)): comma separated numbers or list of numbers in E164 format
            body(str)       : text message body
            mediaUrl(str)   : list of URL's of attachments of the MMS message.
            subject(str)    : utf-encoded subject
            reference(str)  : client reference text
            scheduledDatetime(str) : scheduled date time in RFC3339 format
        Raises:
            ErrorException:  On api returning errors

        Returns:
            MMS: On success an MMS instance instantiated with success response
        """
        if isinstance(recipients, list):
            recipients = ','.join(recipients)
        if isinstance(mediaUrls, str):
            mediaUrls = [mediaUrls]
        params = locals()
        del (params['self'])
        return MMS().load(self.request('mms', 'POST', params))

    def voice_message(self, id):
        "Retrieve the information of a specific voice message."
        return VoiceMessage().load(self.request('voicemessages/' + str(id)))

    def voice_message_list(self, limit=10, offset=0):
        "Retrieve the information of a list of voice messages."
        query = self._format_query(limit, offset)
        return VoiceMessagesList().load(self.request('voicemessages?' + query, 'GET', None))

    def voice_message_create(self, recipients, body, params=None):
        """Create a new voice message."""
        if params is None:
            params = {}
        if type(recipients) == list:
            recipients = ','.join(recipients)

        params.update({'recipients': recipients, 'body': body})
        return VoiceMessage().load(self.request('voicemessages', 'POST', params))

    def lookup(self, phonenumber, params=None):
        """Do a new lookup."""
        if params is None:
            params = {}
        return Lookup().load(self.request('lookup/' + str(phonenumber), 'GET', params))

    def lookup_hlr(self, phonenumber, params=None):
        """Retrieve the information of a specific HLR lookup."""
        if params is None:
            params = {}
        return HLR().load(self.request('lookup/' + str(phonenumber) + '/hlr', 'GET', params))

    def lookup_hlr_create(self, phonenumber, params=None):
        """Perform a new HLR lookup."""
        if params is None:
            params = {}
        return HLR().load(self.request('lookup/' + str(phonenumber) + '/hlr', 'POST', params))

    def verify(self, id):
        """Retrieve the information of a specific verification."""
        return Verify().load(self.request('verify/' + str(id)))

    def verify_create(self, recipient, params=None):
        """Create a new verification."""
        if params is None:
            params = {}
        params.update({'recipient': recipient})
        return Verify().load(self.request('verify', 'POST', params))

    def verify_create_email(self, recipient, originator, params=None):
        """Create a new email verification."""
        if params is None:
            params = {}
        params.update({
            'type': 'email',
            'recipient': recipient,
            'originator': originator
        })
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
        if params is None:
            params = {}
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
        if params is None:
            params = {}
        params.update({'name': name})
        return Group().load(self.request('groups', 'POST', params))

    def group_delete(self, id):
        self.request_plain_text('groups/' + str(id), 'DELETE', None)

    def group_list(self, limit=10, offset=0):
        query = self._format_query(limit, offset)
        return GroupList().load(self.request('groups?' + query, 'GET', None))

    def group_update(self, id, name, params=None):
        if params is None:
            params = {}
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
        uri = self.generate_voice_calls_url(call_id=call_id, leg_id=leg_id)
        return VoiceRecordingsList().load(self.request(uri, 'GET'))

    def voice_transcription_list(self, call_id, leg_id, recording_id):
        """List voice transcriptions."""
        uri = self.generate_voice_calls_url(call_id, leg_id, recording_id)
        return VoiceTranscriptionsList().load(self.request(uri, 'GET'))

    def voice_transcription_download(self, call_id, leg_id, recording_id, transcriptions_file):
        """Download voice transcription file."""
        uri = self.generate_voice_calls_url(call_id, leg_id, recording_id) + '/' + str(transcriptions_file)
        return self.request(uri, 'GET')

    def voice_transcription_view(self, call_id, leg_id, recording_id, transcriptions_id):
        """Get voice transcription data."""
        uri = self.generate_voice_calls_url(call_id, leg_id, recording_id) + '/' + str(transcriptions_id)
        return VoiceTranscriptionsView().load(self.request(uri, 'GET'))

    def voice_transcription_create(self, call_id, leg_id, recording_id, language):
        """Create a voice transcription."""
        uri = self.generate_voice_calls_url(call_id, leg_id, recording_id)
        params = {'language': str(language)}
        return VoiceTranscriptionsView().load(self.request(uri, 'POST', params, VOICE_TYPE))

    def voice_recording_view(self, call_id, leg_id, recording_id):
        uri = self.generate_voice_calls_url(call_id=call_id, leg_id=leg_id) + '/' + str(recording_id)
        recording_response = self.request(uri, 'GET')
        recording_links = recording_response.get('_links')
        if recording_links is not None:
            recording_response['data'][0]['_links'] = recording_links
        return VoiceRecording().load(recording_response['data'][0])

    def voice_recording_delete(self, call_id, leg_id, recording_id):
        uri = self.generate_voice_calls_url(call_id=call_id, leg_id=leg_id) + '/' + str(recording_id)
        recording_response = self.request(uri, 'DELETE', None, VOICE_TYPE)

    def voice_recording_download(self, call_id, leg_id, recording_id):
        uri = self.generate_voice_calls_url(call_id=call_id, leg_id=leg_id) + '/' + str(recording_id)
        recording_response = self.request(uri, 'GET')
        recording_links = recording_response.get('_links')
        if recording_links is None or recording_links.get('file') is None:
            raise (ErrorException('There is no recording available'))
        recording_file = recording_links.get('file')
        recording_file = self.request_store_as_file(VOICE_API_ROOT + recording_file, recording_id + '.wav')
        return VOICE_API_ROOT + recording_file

    def voice_read_webhook(self, id):
        """
        Retrieve a voice webhook
        API Reference: https://developers.messagebird.com/api/voice-calling/#webhooks
        """
        uri = VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '/' + str(id)
        return VoiceWebhook().load(self.request(uri, 'GET', None, VOICE_TYPE))

    def voice_list_webhooks(self, limit=10, offset=0):
        """ Retrieve a list of voice webhooks. """
        uri = VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '?' + self._format_query(limit, offset)
        return VoiceWebhookList().load(self.request(uri, 'GET', None, VOICE_TYPE))

    def voice_create_webhook(self, create_webhook_request):
        """ Create a voice webhook. """
        if create_webhook_request is None:
            raise ValidationError('Create request is empty')

        uri = VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH
        return VoiceWebhook().load(self.request(uri, 'POST', create_webhook_request.__dict__(), VOICE_TYPE))

    def voice_update_webhook(self, id, update_webhook_request):
        """ Update a voice webhook. """
        if update_webhook_request is None:
            raise ValidationError('Update request is empty')

        uri = VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '/' + str(id)
        return VoiceWebhook().load(self.request(uri, 'PUT', update_webhook_request.__dict__(), VOICE_TYPE))

    def voice_delete_webhook(self, id):
        """ Delete a voice webhook. """
        uri = VOICE_API_ROOT + '/' + VOICE_WEB_HOOKS_PATH + '/' + str(id)
        self.request(uri, 'DELETE', None, VOICE_TYPE)

    def call_flow(self, id):
        return CallFlow().load(self.request('call-flows/' + str(id), 'GET', None, VOICE_TYPE))

    def call_flow_list(self, limit=10, offset=0):
        query = self._format_query(limit, offset)
        return CallFlowList().load(self.request('call-flows?' + query, 'GET', None, VOICE_TYPE))

    def call_flow_create(self, steps, default=False, record=False, title=None):
        params = {'steps': steps, 'default': default, 'record': record}
        if title is not None:
            params['title'] = title
        return CallFlow().load(self.request('call-flows', 'POST', params, VOICE_TYPE))

    def call_flow_update(self, id, steps, default, record, title=None):
        params = {'steps': steps, 'default': default, 'record': record}
        if title is not None:
            params['title'] = title
        return CallFlow().load(self.request('call-flows/' + str(id), 'PUT', params, VOICE_TYPE))

    def call_flow_delete(self, id):
        self.request_plain_text('call-flows/' + str(id), 'DELETE', None, VOICE_TYPE)

    def call_flow_numbers_list(self, call_flow_id):
        return CallFlowNumberList().load(
            self.request('call-flows/' + str(call_flow_id) + '/numbers', 'GET', None, VOICE_TYPE))

    def call_flow_numbers_add(self, call_flow_id, numbers=()):
        params = {'numbers': numbers}
        return CallFlowNumberList().load(
            self.request('call-flows/' + str(call_flow_id) + '/numbers', 'POST', params, VOICE_TYPE))

    def _format_query(self, limit, offset):
        return 'limit=' + str(limit) + '&offset=' + str(offset)

    def available_numbers_list(self, country, params={}, limit=20, offset=0):
        """Retrieve a list of phone numbers available for purchase."""
        params['limit'] = limit
        params['offset'] = offset
        return NumberList().load(self.request(NUMBER_AVAILABLE_PATH + '/' + str(country), 'GET', params, NUMBER_TYPE))

    def purchase_number(self, number, country, billingIntervalMonths=1):
        params = {'number': str(number), 'countryCode': str(country), 'billingIntervalMonths': int(billingIntervalMonths)}
        return Number().load(self.request(NUMBER_PATH, 'POST', params, NUMBER_TYPE))

    def update_number(self, number, tags):
        params = {'tags': tags}
        return Number().load(self.request(NUMBER_PATH + '/' + str(number), 'PATCH', params, NUMBER_TYPE))

    def delete_number(self, number):
        self.request(NUMBER_PATH + '/' + str(number), 'DELETE', None, NUMBER_TYPE)

    def purchased_numbers_list(self, params={}, limit=20, offset=0):
        params['limit'] = limit
        params['offset'] = offset
        return NumberList().load(self.request(NUMBER_PATH, 'GET', params, NUMBER_TYPE))

    def purchased_number(self, number):
        return Number().load(self.request(NUMBER_PATH + '/' + number, 'GET', None, NUMBER_TYPE))

    @staticmethod
    def generate_voice_calls_url(call_id=None, leg_id=None, recording_id=None):
        uri = VOICE_API_ROOT + '/' + VOICE_PATH + '/'
        uri += str(call_id) + '/' + VOICE_LEGS_PATH + '/' + str(leg_id) + '/' + VOICE_RECORDINGS_PATH
        if recording_id:
            uri += '/' + str(recording_id) + '/' + VOICE_TRANSCRIPTIONS_PATH
        return uri
