# tests.test_utils.py

# pylint: disable=C0114,C0116,W0621,W0212

import ipaddress
from collections import OrderedDict
from datetime import datetime
from xml.parsers.expat import ExpatError

import pytest
import pytz

from pyonms import utils


def test_convert_time():
    # Test if value is `None`
    assert utils.convert_time(time=None) is None

    # Test if value is valid millisecond timestamp
    converted_time = utils.convert_time(time=1704904715000)
    assert isinstance(converted_time, datetime)

    # Test if value is not a valid data type
    with pytest.raises(ValueError, match="Time value not an integer"):
        utils.convert_time(time="now")


def test_convert_time_with_zone():
    # Test for valid parameters
    converted_time = utils.convert_time(time=1704904715000, zone="US/Eastern")
    assert isinstance(converted_time, datetime)
    converted_time = utils.convert_time(
        time=1704904715000, zone=pytz.timezone("US/Eastern")
    )
    assert isinstance(converted_time, datetime)

    # Test for invalid timezone
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError, match="'Apex'"):
        utils.convert_time(time=1704904715000, zone="Apex")
    with pytest.raises(ValueError, match="Timezone is not a valid type"):
        utils.convert_time(time=1704904715000, zone=1245)


def test_convert_link_time():
    # Test if value is `None`
    assert utils.convert_link_time(time=None) is None

    # Test if value is valid enlinkd time string
    converted_time = utils.convert_link_time(time="01/01/24, 12:00:00 am")
    assert isinstance(converted_time, datetime)

    # Test if value is not valid enlinkd time string
    time_values = ["now", 1704904715000]
    for time_value in time_values:
        with pytest.raises(
            ValueError,
            match=f"time data '{time_value}' does not match format '{utils.LINK_TIME_PATTERN}'",
        ):
            utils.convert_link_time(time=time_value)


def test_convert_link_time_with_zone():
    # Test for valid parameters
    converted_time = utils.convert_link_time(
        time="01/01/24, 12:00:00 am", zone="US/Eastern"
    )
    assert isinstance(converted_time, datetime)
    converted_time = utils.convert_link_time(
        time="01/01/24, 12:00:00 am", zone=pytz.timezone("US/Eastern")
    )
    assert isinstance(converted_time, datetime)

    # Test for invalid timezone
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError, match="'Apex'"):
        utils.convert_link_time(time="01/01/24, 12:00:00 am", zone="Apex")
    with pytest.raises(ValueError, match="Timezone is not a valid type"):
        utils.convert_link_time(time="01/01/24, 12:00:00 am", zone=12345)


def test_convert_xml():
    # Test for valid XML
    source = """
    <nodes>
        <node label="name">
            <interface>int1</interface>
            <interface>int2</interface>
        </node>
        <node label="name2"/>
    </nodes>"""
    destination = {
        "nodes": {
            "node": [
                {"interface": ["int1", "int2"], "label": "name"},
                {"label": "name2"},
            ]
        }
    }
    conversion = utils.convert_xml(data=source)
    assert isinstance(conversion, dict)
    assert conversion == destination

    # Test for invalid XML
    with pytest.raises(ExpatError):
        assert utils.convert_xml("hello")


def test_normalize_dict():
    source = OrderedDict(
        {
            "nodes": {
                "node": [
                    OrderedDict({"@label": "name", "interface": ["int1", "int2"]}),
                    OrderedDict({"@label": "name2"}),
                ]
            }
        }
    )
    destination = {
        "nodes": {
            "node": [
                {"label": "name", "interface": ["int1", "int2"]},
                {"label": "name2"},
            ]
        }
    }

    assert utils.normalize_dict(source) == destination
    assert utils.normalize_dict(["a", "b"]) == ["a", "b"]
    assert utils.normalize_dict(["@a", "@b"]) == ["@a", "@b"]
    assert utils.normalize_dict(["a@", "b@"]) == ["a@", "b@"]


def test_normalize_key():
    assert utils.normalize_key(key="testing") == "testing"
    assert utils.normalize_key(key="this_is_a_test") == "this_is_a_test"
    assert utils.normalize_key(key="this-is-a-test") == "this_is_a_test"
    assert utils.normalize_key(key="@testing") == "testing"
    assert utils.normalize_key(key="@testing@things") == "testing@things"
    assert utils.normalize_key(key="testing") == "testing"


def test_check_ip():
    assert utils.check_ip_address("127.0.0.1") == True
    assert utils.check_ip_address("500.500.500.500") == False
    assert utils.check_ip_address("2001:abcd::1") == True
    assert utils.check_ip_address("invalid") == False
    with pytest.raises(ipaddress.AddressValueError):
        assert utils.check_ip_address("invalid", raise_error=True)
