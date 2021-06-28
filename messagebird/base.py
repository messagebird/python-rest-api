from datetime import datetime

import dateutil.parser
import json


class Base:
    def load(self, data):
        if data is not None:
            for name, value in list(data.items()):
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

        return self

    @staticmethod
    def value_to_time(value, format='%Y-%m-%dT%H:%M:%S+00:00'):
        if value is not None:
            return dateutil.parser.parse(value).replace(microsecond=0)
