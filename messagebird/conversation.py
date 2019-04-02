from messagebird.base import Base
from messagebird.conversation_contact import ConversationContact
from messagebird.conversation_channel import Channel

CONVERSATION_STATUS_ACTIVE = "active"
CONVERSATION_STATUS_ARCHIVED = "archived"


class Conversation(Base):

    def __init__(self):
        self.id = None
        self.contactId = None
        self._contact = None
        self.lastUsedChannelId = None
        self.channels = None
        self.messages = None
        self.status = None
        self._createdDateTime = None
        self._updatedDateTime = None
        self._lastReceivedDateTime = None

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        self._contact = ConversationContact().load(value)

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value):
        if isinstance(value, list):
            self._channels = []
            for channelData in value:
                self._channels.append(Channel().load(channelData))
        else:
            self._channels = value

    @property
    def createdDateTime(self):
        return self._createdDateTime

    @createdDateTime.setter
    def createdDateTime(self, value):
        self._createdDateTime = self.value_to_time(value)

    @property
    def updatedDateTime(self):
        return self._updatedDateTime

    @updatedDateTime.setter
    def updatedDateTime(self, value):
        self._updatedDateTime = self.value_to_time(value)

    @property
    def lastReceivedDateTime(self):
        return self._lastReceivedDateTime

    @lastReceivedDateTime.setter
    def lastReceivedDateTime(self, value):
        self._lastReceivedDateTime = self.value_to_time(value)