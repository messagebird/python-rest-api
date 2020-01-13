from messagebird.base import Base
from messagebird.base_list import BaseList


class NumberList(BaseList):
    def __init__(self):
        # We're expecting items of type Number
        super(NumberList, self).__init__(Number)


class Number(Base):
    def __init__(self):
        self.number = None
        self.country = None
        self.region = None
        self.locality = None
        self.features = None
        self.tags = None
        self.type = None
        self.status = None
