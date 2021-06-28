import json


def json_serialize(obj):
    try:
        return json.dumps(obj, ensure_ascii=False).encode('utf-8')
    except TypeError:
        return json.dumps(obj, default=lambda o: o.__dict__, ensure_ascii=False).encode('utf-8')
