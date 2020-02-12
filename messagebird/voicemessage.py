from messagebird.base import Base
from messagebird.base_list import BaseList
from messagebird.recipient import Recipient


class VoiceMessagesList(BaseList):
    def __init__(self):
        super(VoiceMessagesList, self).__init__(VoiceMessage)
        self.perPage = None
        self.currentPage = None
        self.pageCount = None
        self._pagination = None

    @property
    def data(self):
        return self.items

    @property
    def pagination(self):
        return {
            "totalCount": self.totalCount,
            "pageCount": self.pageCount,
            "currentPage": self.currentPage,
            "perPage": self.perPage
        }

    @pagination.setter
    def pagination(self, value):
        if isinstance(value, dict):
            self.totalCount = value['totalCount']
            self.pageCount = value['pageCount']
            self.currentPage = value['currentPage']
            self.perPage = value['perPage']
            self.limit = self.perPage * self.currentPage
            self.offset = self.perPage * (self.currentPage - 1)

    @data.setter
    def data(self, value):
        if isinstance(value, list):
            self.count = len(value)
            self.items = value


class VoiceMessage(Base):
    def __init__(self):
        self.id = None
        self.href = None
        self.originator = None
        self.body = None
        self.reference = None
        self.language = None
        self.voice = None
        self.repeat = None
        self.ifMachine = None
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
