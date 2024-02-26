# utils.__init__.py

"""Helper Utilities"""

import ipaddress
from collections import OrderedDict
from datetime import datetime, tzinfo
from typing import Optional, Union

import pytz
import xmltodict

LINK_TIME_PATTERN = "%m/%d/%y, %I:%M:%S %p"


def convert_time(
    time: int, zone: Optional[Union[str, tzinfo]] = None
) -> Optional[datetime]:
    """Convert epoch to `datetime`"""
    if not time:
        return None
    if isinstance(time, int):
        time_stamp = datetime.fromtimestamp(time / 1000)
        if isinstance(zone, str):
            time_stamp.replace(tzinfo=pytz.timezone(zone))
        elif isinstance(zone, tzinfo):
            time_stamp.replace(tzinfo=zone)
        elif zone:
            raise ValueError("Timezone is not a valid type")
        return time_stamp
    else:
        raise ValueError("Time value not an integer")


def convert_link_time(
    time: str, zone: Optional[Union[str, tzinfo]] = None
) -> Optional[datetime]:
    """Convert enlinkd time to `datetime`"""
    if not time:
        return None
    if isinstance(time, str):
        link_time = datetime.strptime(time, LINK_TIME_PATTERN)
        if isinstance(zone, str):
            link_time.replace(tzinfo=pytz.timezone(zone))
        elif isinstance(zone, tzinfo):
            link_time.replace(tzinfo=zone)
        elif zone:
            raise ValueError("Timezone is not a valid type")
        return link_time
    else:
        raise ValueError(
            f"time data '{time}' does not match format '{LINK_TIME_PATTERN}'"
        )


def convert_xml(data: str) -> dict:
    """Parse XML string into a `dict`"""
    parsed_data = xmltodict.parse(data)
    return dict(normalize_dict(parsed_data))


def normalize_dict(data: Union[OrderedDict, dict, list]) -> Union[dict, list]:
    """Convert `OrderedDict` into a standard `dict`"""
    if isinstance(data, (OrderedDict, dict)):
        cleaned = {}
        for key, value in data.items():
            if isinstance(value, (OrderedDict, dict)):
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


def check_ip_address(ip: str, raise_error: bool = False):
    """Check string for valid IP address"""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        try:
            ipaddress.IPv6Address(ip)
            return True
        except ipaddress.AddressValueError:
            if raise_error:
                raise ipaddress.AddressValueError
            else:
                return False
