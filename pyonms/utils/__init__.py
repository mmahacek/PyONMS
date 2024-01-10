# utils.__init__.py

"""Helper Utilities"""

from collections import OrderedDict
from datetime import datetime, timezone
from typing import Union

import pytz
import xmltodict


def convert_time(time: int, zone: str = None) -> datetime:
    """Convert epoch to `datetime`"""
    if isinstance(time, int):
        time_stamp = datetime.fromtimestamp(time / 1000)
        if isinstance(zone, str):
            time_stamp.replace(tzinfo=pytz.timezone(zone))
        elif isinstance(zone, timezone):
            time_stamp.replace(tzinfo=zone)
        return time_stamp
    else:
        raise ValueError


def convert_link_time(time: str, zone: Union[str, timezone] = None) -> datetime:
    """Convert enlinkd time to `datetime`"""
    if isinstance(time, str):
        pattern = "%m/%d/%y, %I:%M:%S %p"
        link_time = datetime.strptime(time, pattern)
        if isinstance(zone, str):
            link_time.replace(tzinfo=pytz.timezone(zone))
        elif isinstance(zone, timezone):
            link_time.replace(tzinfo=zone)
        return link_time
    else:
        raise ValueError


def convert_xml(data: str) -> dict:
    """Parse XML string into a `dict`"""
    data = xmltodict.parse(data)
    return normalize_dict(data)


def normalize_dict(data: Union[OrderedDict, dict]) -> dict:
    """Convert `OrderedDict` into a standard `dict`"""
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
    """Replace XML characters"""
    if key[0] == "@":
        key = key[1:]
    return key.replace("-", "_")
