import json


def read_json(filepath):
    with open(filepath) as json_file:
        return json.load(json_file)
