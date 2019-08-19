from messagebird.base import Base


class Webhook(Base):

    def __init__(self):
        self.url = None
        self.token = None
