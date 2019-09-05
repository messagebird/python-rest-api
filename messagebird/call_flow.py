from messagebird.base import Base
from messagebird.base_list import BaseList


class CallFlowList(BaseList):

    def __init__(self):
        # Signal the BaseList that we're expecting items of type Group...
        super(CallFlowList, self).__init__(CallFlow)


class CallFlow(Base):

    def __init__(self):
        self.id = None
        self.title = None
        self.record = None
        self.steps = None
        self._createdAt = None
        self._updatedAt = None

    @property
    def created_at(self):
        return self._createdAt

    @created_at.setter
    def created_at(self, value):
        self._createdAt = self.value_to_time(value)

    @property
    def updated_at(self):
        return self._updatedAt

    @updated_at.setter
    def updated_at(self, value):
        self._updatedAt = self.value_to_time(value)

    def load(self, data):
        for name, value in list(data.get('data')[0].items()):
            if hasattr(self, name) and not callable(getattr(self, name)):
                setattr(self, name, value)

        return self
