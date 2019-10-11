from messagebird.base import Base
from messagebird.base_list import BaseList


class CallFlowList(BaseList):

    def __init__(self):
        self._data = None
        self._pagination = None

        super(CallFlowList, self).__init__(CallFlow)

    @property
    def data(self):
        return self._data

    @property
    def pagination(self):
        return self._pagination

    @pagination.setter
    def pagination(self, value):
        self._pagination = value

    @data.setter
    def data(self, value):
        """Create typed objects from the dicts."""
        items = []
        for item in value:
            items.append(self.itemType().load(item))

        self._data = items


class CallFlowNumberList(BaseList):
    def __init__(self):
        self._data = None
        self._pagination = None

        super(CallFlowNumberList, self).__init__(CallFlowNumber)

    @property
    def data(self):
        return self._data

    @property
    def pagination(self):
        return self._pagination

    @pagination.setter
    def pagination(self, value):
        self._pagination = value

    @data.setter
    def data(self, value):
        """Create typed objects from the dicts."""
        items = []
        for item in value:
            items.append(self.itemType().load(item))

        self._data = items


class CallFlow(Base):

    def __init__(self):
        self.id = None
        self.title = None
        self.record = None
        self.steps = None
        self.default = None
        self._createdAt = None
        self._updatedAt = None

    @property
    def createdAt(self):
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.value_to_time(value)

    @property
    def updatedAt(self):
        return self._updatedAt

    @updatedAt.setter
    def updatedAt(self, value):
        self._updatedAt = self.value_to_time(value)

    def load(self, data):
        if data.get('data') is not None:
            items = data.get('data')[0].items()
        else:
            items = list(data.items())

        for name, value in items:
            if hasattr(self, name) and not callable(getattr(self, name)):
                setattr(self, name, value)

        return self


class CallFlowNumber(Base):
    def __init__(self):
        self.id = None
        self.number = None
        self.callFlowId = None
        self._createdAt = None
        self._updatedAt = None

    @property
    def createdAt(self):
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.value_to_time(value)

    @property
    def updatedAt(self):
        return self._updatedAt

    @updatedAt.setter
    def updatedAt(self, value):
        self._updatedAt = self.value_to_time(value)

    def load(self, data):
        if data.get('data') is not None:
            items = data.get('data')[0].items()
        else:
            items = list(data.items())

        for name, value in items:
            if hasattr(self, name) and not callable(getattr(self, name)):
                setattr(self, name, value)

        return self
