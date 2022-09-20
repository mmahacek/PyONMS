# models.alarm.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Union

from pyonms.models.event import Event, EventParameter, Severity
from pyonms.models.node import ServiceType
from pyonms.utils import convert_time


@dataclass(repr=False)
class Alarm:
    id: int
    uei: str
    location: str
    type: int
    severity: Severity
    description: str
    logMessage: str
    suppressedUntil: datetime
    suppressedTime: datetime
    x733ProbableCause: int
    affectedNodeCount: int
    reductionKey: str
    count: int
    firstEventTime: datetime
    lastEventTime: datetime = None
    nodeId: int = None
    nodeLabel: str = None
    ipAddress: str = None
    ifIndex: int = None
    clearKey: str = None
    firstEvent: Union[Event, None] = field(default_factory=dict)
    lastEvent: Union[Event, None] = field(default_factory=dict)
    parameters: List[Union[EventParameter, None]] = field(default_factory=list)
    serviceType: ServiceType = field(default_factory=dict)

    def __post_init__(self):
        self.suppressedUntil = convert_time(self.suppressedUntil)
        self.suppressedTime = convert_time(self.suppressedTime)
        self.firstEventTime = convert_time(self.firstEventTime)
        self.lastEventTime = convert_time(self.lastEventTime)
        self.severity = Severity[self.severity]
        if self.lastEvent:
            self.lastEvent = Event(**self.lastEvent)
        self.parameters = [EventParameter(**parameter) for parameter in self.parameters]
        if self.serviceType:
            self.serviceType = ServiceType(**self.serviceType)

    def __repr__(self):
        return f"Alarm(id={self.id}, reductionKey={self.reductionKey})"
