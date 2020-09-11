import json
import sys


def json_serialize(obj):
    if sys.version_info > (3, 0):
        try:
            return json.dumps(obj, ensure_ascii=False).encode('utf-8')
        except TypeError:
            return json.dumps(obj, default=lambda o: o.__dict__, ensure_ascii=False).encode('utf-8')
    else:
        try:
            return json.dumps(obj, ensure_ascii=False, encoding='utf-8')
        except TypeError:
            return json.dumps(obj, default=lambda o: o.__dict__, ensure_ascii=False, encoding='utf-8')
