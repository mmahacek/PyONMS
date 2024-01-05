# tests.test_events.py

# pylint: disable=C0114,C0116,W0621

from datetime import datetime

import pytest

from pyonms import PyONMS
from pyonms.models.event import Event, Severity


@pytest.fixture()
def test_event(test_instance: PyONMS) -> Event:
    return test_instance.events.get_event(id=317)


@pytest.mark.vcr()
def test_event_one(test_event: Event):
    assert isinstance(test_event, Event)
    assert test_event.id == 317
    assert test_event.uei == "uei.opennms.org/threshold/highThresholdExceeded"
    assert test_event.parameters["resourceType"].value == "hrStorageIndex"
    assert isinstance(test_event.createTime, datetime)
    assert test_event.display
    assert test_event.log
    assert test_event.severity == Severity.WARNING


@pytest.mark.vcr()
def test_event_all(test_instance: PyONMS):
    events = test_instance.events.get_events(limit=1000)
    assert len(events) == 287
    assert events[0].id == 319
    assert events[0].uei == "uei.opennms.org/threshold/highThresholdExceeded"
    assert events[0].parameters["resourceType"].value == "if"


@pytest.mark.vcr()
def test_event_batch(test_instance: PyONMS):
    events = test_instance.events.get_events(limit=20, batch_size=5)
    assert len(events) == 20
    assert events[0].id == 319
    assert events[0].uei == "uei.opennms.org/threshold/highThresholdExceeded"
    assert events[0].parameters["resourceType"].value == "if"
