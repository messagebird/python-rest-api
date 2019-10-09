from messagebird.base import Base


class VoiceRecording(Base):

    def __init__(self):
        self.id = None
        self.format = None
        self.type = None
        self.legId = None
        self.status = None
        self.duration = None
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
            'recording id           : %s' % self.id,
            'format            : %s' % self.format,
            'type              : %s' % self.type,
            'leg id            : %s' % self.legId,
            'status            : %s' % self.status,
            'duration          : %s' % self.duration,
            'created date time : %s' % self._createdDatetime,
            'updated date time : %s' % self._updatedDatetime,
            'links             : %s' % self._links
        ])


class VoiceRecordingsList(Base):
    def __init__(self):
        self._items = None

    @property
    def data(self):
        return self._items

    @data.setter
    def data(self, value):
        if isinstance(value, list):
            self._items = []
            for item in value:
                self._items.append(VoiceRecording().load(item))

    def __str__(self):
        item_ids = []
        if self._items is not None:
            for recording_item in self._items:
                item_ids.append(recording_item.id)

        return "\n".join([
            'items IDs  : %s' % item_ids,
            'count      : %s' % len(item_ids)
        ])
