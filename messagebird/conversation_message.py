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
        self.createdDateTime = None
        self.updatedDateTime = None


class ConversationMessageList(Base):

    def __init__(self):
        self.offset = None
        self.limit = None
        self.count = None
        self.totalCount = None
        self.items = None


class ConversationMessageCreateRequest(Base):

    def __init__(self):
        self.channelId = None
        self.content = None
        self.type = None
