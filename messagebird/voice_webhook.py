from messagebird.base import Base
from messagebird.validation import validate_is_not_blank


class VoiceWebhook(Base):

    def __init__(self):
        self.id = None
        self.url = None
        self.token = None
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

    def load(self, data):
        if data.get('data') is not None:
            items = data.get('data')[0].items()
        else:
            items = list(data.items())

        for name, value in items:
            if hasattr(self, name) and not callable(getattr(self, name)):
                setattr(self, name, value)

        return self

    def __str__(self):
        return "\n".join([
            'webhook id         : %s' % self.id,
            'url                : %s' % self.url,
            'token              : %s' % self.token,
            'created date time  : %s' % self._createdDatetime,
            'updated date time  : %s' % self._updatedDatetime,
            'links              : %s' % self._links
        ])


class VoiceWebhookList(Base):

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
                self._items.append(VoiceWebhook().load(item))

    def __str__(self):
        item_ids = []
        if self._items is not None:
            for voice_item in self._items:
                item_ids.append(voice_item.id)

        return "\n".join([
            'items IDs  : %s' % item_ids,
            'count      : %s' % len(item_ids)
        ])


class VoiceCreateWebhookRequest(object):

    def __init__(self, title=None, url=None, token=None):
        validate_is_not_blank(title, "title cannot be empty")
        validate_is_not_blank(url, "url cannot be empty")
        self._title = title
        self._url = url
        self.token = token

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        validate_is_not_blank(value, "title cannot be empty")
        self._title = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        validate_is_not_blank(value, "url cannot be empty")
        self._url = value

    def __str__(self):
        return "\n".join([
            'title  : %s' % self.title,
            'url  : %s' % self.url,
            'token  : %s' % self.token,
        ])


class VoiceUpdateWebhookRequest(object):

    def __init__(self, title=None, token=None):
        self.title = title
        self.token = token

    def __str__(self):
        return "\n".join([
            'title  : %s' % self.title,
            'token  : %s' % self.token,
        ])
