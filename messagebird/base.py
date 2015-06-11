from datetime import datetime

class Base(object):
  def load(self, data):
    for name, value in data.items():
      if hasattr(self, name):
        setattr(self, name, value)

    return self

  def value_to_time(self, value):
    if value != None:
      return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+00:00')
