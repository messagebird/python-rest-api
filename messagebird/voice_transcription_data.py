from messagebird.base import Base


class VoiceTranscriptionData(Base):

    def __init__(self):
        self.id = None
        self.recordingId = None
        self.legId = None
        self.status = None
        self._createdDatetime = None
        self._updatedDatetime = None
        self._links = None

    @property
    def createdDatetime(self):
        return self._createdDatetime

    @createdDatetime.setter
    def createdAt(self, value):
        if value is not None:
            self._createdDatetime = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def updatedDatetime(self):
        return self._updatedDatetime

    @updatedDatetime.setter
    def updatedAt(self, value):
        if value is not None:
            self._updatedDatetime = self.value_to_time(value, '%Y-%m-%dT%H:%M:%SZ')

    def __str__(self):
        return "\n".join([
            'id                 : %s' % self.id,
            'recording id       : %s' % self.recordingId,
            'status             : %s' % self.status,
            'leg id             : %s' % self.legId,
            'created date time  : %s' % self._createdDatetime,
            'updated date time  : %s' % self._updatedDatetime,
            'links              : %s' % self._links
        ])
