from messagebird.base      import Base
from messagebird.recipient import Recipient
from messagebird.message import Message

class Verify(Base):
  def __init__(self):
    self.id                 = None
    self.href               = None
    self.type               = None 
    self.originator         = None 
    self.reference          = None 
    self.template           = None
    self.timeout            = None
    self.tokenLength        = None
    self.voice              = None
    self.language           = None
    self.status             = None
    self._createdDatetime   = None
    self._validUntilDatetime= None
    self._recipient         = None
    self._messages          = None


  @property
  def createdDatetime(self):
    return self._createdDatetime

  @createdDatetime.setter
  def createdDatetime(self, value):
    self._createdDatetime = self.value_to_time(value)


  @property
  def validUntilDatetime(self):
    return self._validUntilDatetime

  @validUntilDatetime.setter
  def validUntilDatetime(self, value):
    self._validUntilDatetime = self.value_to_time(value)    

  @property
  def recipient(self):
    return self._recipient

  @recipient.setter
  def recipient(self, value):
    self._recipient = Recipient().load(value)

  @property
  def messages(self):
    return self._messages

  @messages.setter
  def messages(self, value):
    value['items'] = [Message().load(r) for r in value['items']]
    self._messages = value 
