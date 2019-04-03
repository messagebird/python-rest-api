from messagebird.base import Base

CONVERSATION_WEBHOOK_EVENT_CONVERSATION_CREATED = 'conversation.created'
CONVERSATION_WEBHOOK_EVENT_CONVERSATION_UPDATED = 'conversation.updated'
CONVERSATION_WEBHOOK_EVENT_MESSAGE_CREATED = 'message.created'
CONVERSATION_WEBHOOK_EVENT_MESSAGE_UPDATED = 'message.updated'


class ConversationWebhook(Base):

    def __init__(self):
        self.id = None
        self.channelId = None
        self.url = None
        self.events = None
        self._createdDatetime = None
        self._updatedDatetime = None

    @property
    def createdDatetime(self):
        return self._createdDatetime

    @createdDatetime.setter
    def createdDatetime(self, value):
        self._createdDatetime = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def updatedDatetime(self):
        return self._updatedDatetime

    @updatedDatetime.setter
    def updatedDatetime(self, value):
        self._updatedDatetime = self.value_to_time(value)