from messagebird.base import Base
from messagebird.call_data import CallData

CALL_STATUS_STARTING = "starting"
CALL_STATUS_ONGOING = "ongoing"
CALL_STATUS_ENDED = "ended"


class Call(Base):

    def __init__(self):
        self.id = None
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = CallData().load(value[0])

    def __str__(self):
        return "\n".join([
            'id                 : %s' % self.id,
            'data.' + 'data.'.join(str(self._data).splitlines(True)),
        ])
