# tests.test_alarms.py

# pylint: disable=C0114,C0116,W0621,W0212

from datetime import datetime

import pytest

from pyonms import PyONMS
from pyonms.models.alarm import Alarm
from pyonms.models.event import Event, Severity


@pytest.mark.vcr()
def test_alarm_one(test_instance: PyONMS):
    test_alarm = test_instance.alarms.get_alarm(id=66)
    assert isinstance(test_alarm, Alarm)
    assert test_alarm.id == 66
    assert test_alarm.lastEvent.id == 281
    assert test_alarm.serviceType.id == 6
    assert test_alarm.count == 2
    assert test_alarm.severity == Severity.MINOR
    assert isinstance(test_alarm.lastEventTime, datetime)
    assert isinstance(test_alarm.lastEvent, Event)


@pytest.mark.vcr()
def test_alarm_all(test_instance: PyONMS):
    alarms = test_instance.alarms.get_alarms(limit=1000)
    assert len(alarms) == 24
    assert alarms[0].id == 76
    assert alarms[0].lastEvent.id == 317
    assert alarms[0].parameters[0].name == "label"


@pytest.mark.vcr()
def test_alarm_batch(test_instance: PyONMS):
    alarms = test_instance.alarms.get_alarms(limit=20, batch_size=5)
    assert len(alarms) == 20
    assert alarms[0].id == 76
    assert alarms[0].lastEvent.id == 317
    assert alarms[0].parameters[0].name == "label"
