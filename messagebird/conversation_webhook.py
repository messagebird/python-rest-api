from messagebird.base import Base

class ConversationWebhookCreateRequest(Base):

    def __init__(self):
        self.channelId = None
        self.events = None
        self.url = None
