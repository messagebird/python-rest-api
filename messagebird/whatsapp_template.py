from messagebird.base import Base
from messagebird.base_list import BaseList


class WhatsAppTemplateList(BaseList):
    def __init__(self):
        # We're expecting items of type WhatsAppTemplate
        super(WhatsAppTemplateList, self).__init__(WhatsAppTemplate)


class WhatsAppTemplate(Base):
    def __init__(self):
        self.name: str = None
        self.language: str = None  # TODO: HSMLanguage object
        self.category: str = None  # TODO: HSMCategory object
        self.components: list = None  # TODO: list of HSMComponent objects
        self.status: str = None  # TODO: HSMStatus object
        self._createdDatetime = None
        self._updatedDatetime = None

    @property
    def createdDatetime(self):
        return self._createdDatetime

    @createdDatetime.setter
    def createdDatetime(self, value):
        self._createdDatetime = self.value_to_time(value)

    @property
    def updatedDatetime(self):
        return self._updatedDatetime

    @updatedDatetime.setter
    def updatedDatetime(self, value):
        self._updatedDatetime = self.value_to_time(value)
