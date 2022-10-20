# utils.__init__.py

from collections import OrderedDict
from datetime import datetime
from typing import Union

import xmltodict


def convert_time(time: int) -> datetime:
    if isinstance(time, int):
        return datetime.utcfromtimestamp(time / 1000)
    else:
        return None


def convert_xml(data: str) -> dict:
    data = xmltodict.parse(data)
    return normalize_dict(data)


def normalize_dict(data: Union[OrderedDict, dict]) -> dict:
    if isinstance(data, Union[OrderedDict, dict]):
        cleaned = {}
        for key, value in data.items():
            if isinstance(value, Union[OrderedDict, dict]):
                cleaned[normalize_key(key)] = normalize_dict(value)
            elif isinstance(value, list):
                cleaned[normalize_key(key)] = [normalize_dict(item) for item in value]
            else:
                cleaned[normalize_key(key)] = value
        return dict(cleaned)
    elif isinstance(data, list):
        return [normalize_dict(item) for item in data]
    else:
        return data


def normalize_key(key: str) -> str:
    if key[0] == "@":
        key = key[1:]
    return key.replace("-", "_")
