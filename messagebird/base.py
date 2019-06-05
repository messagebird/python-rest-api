from datetime import datetime

class Base(object):
  def load(self, data):
    for name, value in list(data.items()):
      if hasattr(self, name) and not callable(getattr(self,name)):
        setattr(self, name, value)

    return self
  
  @staticmethod
  def strip_nanoseconds_from_date(value):
    if str(value).find(".") != -1:
      return value[:-11] + value[-1:]

    return value

  @staticmethod
  def value_to_time(value, format='%Y-%m-%dT%H:%M:%S+00:00'):
    if value is not None:
      value = Base.strip_nanoseconds_from_date(value)
      return datetime.strptime(value, format)