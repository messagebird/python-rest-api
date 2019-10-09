import json


def json_serialize(obj):
    try:
        return json.dumps(obj)
    except TypeError:
        return json.dumps(obj, default=lambda o: o.__dict__)
