import json


def from_arr(arr: list, val):
    lex = {k: val for k in arr}
    return json.dumps(lex)


def from_map(lex: dict):
    return json.dumps(lex)


def to_map(jso: json):
    return json.loads(jso)
