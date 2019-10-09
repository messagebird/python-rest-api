from messagebird.base import Base
from messagebird.recipient import Recipient


class MMS(Base):
    def __init__(self):
        self.id = None
        self.href = None
        self.direction = None
        self.originator = None
        self.subject = None
        self.body = None
        self.mediaUrls = None
        self.reference = None
        self._scheduledDatetime = None
        self._createdDatetime = None
        self._recipients = None

    @property
    def scheduledDatetime(self):
        return self._scheduledDatetime

    @scheduledDatetime.setter
    def scheduledDatetime(self, value):
        self._scheduledDatetime = self.value_to_time(value)

    @property
    def createdDatetime(self):
        return self._createdDatetime

    @createdDatetime.setter
    def createdDatetime(self, value):
        self._createdDatetime = self.value_to_time(value)

    @property
    def recipients(self):
        return self._recipients

    @recipients.setter
    def recipients(self, value):
        value['items'] = [Recipient().load(r) for r in value['items']]
        self._recipients = value

    def __str__(self):
        return "\n".join([
            "id                      : %s" % self.id,
            "href                    : %s" % self.href,
            "direction               : %s" % self.direction,
            "originator              : %s" % self.originator,
            "subject                 : %s" % self.subject,
            "body                    : %s" % self.body,
            "mediaUrls               : %s" % ",".join(self.mediaUrls),
            "reference               : %s" % self.reference,
            "scheduledDatetime       : %s" % self.scheduledDatetime,
            "createdDatetime         : %s" % self.createdDatetime,
            "recipients              : %s" % self.recipients,
        ])
