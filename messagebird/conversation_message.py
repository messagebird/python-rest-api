from messagebird.base import Base

MESSAGE_TYPE_AUDIO = "audio"
MESSAGE_TYPE_FILE = "file"
MESSAGE_TYPE_HSM = "hsm"
MESSAGE_TYPE_IMAGE = "image"
MESSAGE_TYPE_LOCATION = "location"
MESSAGE_TYPE_TEXT = "text"
MESSAGE_TYPE_VIDEO = "video"


class ConversationMessage(Base):

    def __init__(self):
        self.id = None
        self.conversationId = None
        self.channelId = None
        self.direction = None
        self.status = None
        self.type = None
        self.content = None
        self._createdDatetime = None
        self._updatedDatetime = None

    @property
    def createdDatetime(self):
        return self._createdDatetime

    @createdDatetime.setter
    def createdDatetime(self, value):
        if value is not None:
            value = self.strip_nanoseconds_from_date(value)
            self._createdDatetime = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def updatedDatetime(self):
        return self._updatedDatetime

    @updatedDatetime.setter
    def updatedDatetime(self, value):
        if value is not None:
            value = self.strip_nanoseconds_from_date(value)
            self._updatedDatetime = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    def strip_nanoseconds_from_date(self, value):
         return value[:-11] + value[-1:]


class ConversationMessageList(Base):

    def __init__(self):
        self.offset = None
        self.limit = None
        self.count = None
        self.totalCount = None
        self._items = None

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        items = []
        if isinstance(value, list):
            for item in value:
                items.append(ConversationMessage().load(item))

        self._items = items
