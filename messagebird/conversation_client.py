from messagebird.base import Base
from messagebird.client import USER_AGENT, Client
from messagebird.http_client import HttpClient
from messagebird.conversation_message import ConversationMessage, ConversationMessageList
from messagebird.conversation import Conversation, ConversationList
from messagebird.conversation_webhook import ConversationWebhook

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

CONVERSATION_API_ROOT = 'https://conversations.messagebird.com/v1/'
CONVERSATION_PATH = 'conversations'
CONVERSATION_MESSAGES_PATH = 'messages'
CONVERSATION_WEB_HOOKS_PATH = 'webhooks'


class ConversationClient(Base):

    def __init__(self, access_key, http_client=None):
        self.access_key = access_key

        if http_client is None:
            http_client = HttpClient(CONVERSATION_API_ROOT, access_key, USER_AGENT)

        self.client = Client(access_key, http_client)

    def list(self, options=None):
        uri = CONVERSATION_PATH
        if options is not None:
            uri += '?' + urlencode(options)

        return ConversationList().load(self.client.request(uri))

    def start(self, start_request):
        uri = CONVERSATION_PATH + '/start'
        return Conversation().load(self.client.request(uri, 'POST', start_request))

    def update(self, id, update_request):
        uri = CONVERSATION_PATH + '/' + str(id)
        return Conversation().load(self.client.request(uri, 'PATCH', update_request))

    def read(self, id):
        uri = CONVERSATION_PATH + '/' + str(id)
        return Conversation().load(self.client.request(uri))

    def list_messages(self, conversation_id, options=None):
        uri = CONVERSATION_PATH + '/' + str(conversation_id) + '/' + CONVERSATION_MESSAGES_PATH

        if options is not None:
            uri += '?' + urlencode(options)

        return ConversationMessageList().load(self.client.request(uri))

    def create_message(self, conversation_id, message_create_request):
        uri = CONVERSATION_PATH + '/' + str(conversation_id) + '/' + CONVERSATION_MESSAGES_PATH
        return ConversationMessage().load(self.client.request(uri, 'POST', message_create_request))

    def read_message(self, message_id):
        uri = CONVERSATION_MESSAGES_PATH + '/' + str(message_id)
        return ConversationMessage().load(self.client.request(uri))

    def create_webhook(self, webhook_create_request):
        return ConversationWebhook().load(self.client.request(CONVERSATION_WEB_HOOKS_PATH, 'POST', webhook_create_request))

    def delete_webhook(self):
        return self.access_key

    def list_webhooks(self):
        return self.access_key

    def read_webhook(self):
        return self.access_key