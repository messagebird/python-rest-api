from messagebird.base import Base


class Webhook(Base):

    def __init__(self):
        self.url = None
        self.token = None

    def __str__(self):
        return "\n".join([
            'url                : %s' % self.url,
            'token              : %s' % self.token,
        ])
