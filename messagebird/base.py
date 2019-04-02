from datetime import datetime

class Base(object):
  def load(self, data):
    for name, value in list(data.items()):
      if hasattr(self, name):
        setattr(self, name, value)

    return self

  def value_to_time(self, value, format='%Y-%m-%dT%H:%M:%S+00:00'):
    if value != None:
      return datetime.strptime(value, format)
