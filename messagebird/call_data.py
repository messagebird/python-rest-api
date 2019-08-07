from messagebird.base import Base

class CallData(Base):
    
    def __init__(self):
        self.id = None
        self.status = None
        self.source = None
        self.destination = None
        self._createdAt = None
        self._updatedAt = None
        self._endedAt = None


    @property
    def updatedAt(self):
        return self._updatedAt
     
    @updatedAt.setter
    def updatedAt(self, value):
        self._updatedAt = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def createdAt(self):
        return self._createdAt
     
    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def endedAt(self):
        return self._endedAt
     
    @endedAt.setter
    def endedAt(self, value):
        self._endedAt = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')
