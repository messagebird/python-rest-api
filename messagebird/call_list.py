from messagebird.base_list import BaseList
from messagebird.call_data import CallData


class CallList(BaseList):
    def __init__(self):
        # We're expecting items of type CallData
        super(CallList, self).__init__(CallData)
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
