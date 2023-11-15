# models.alarm.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from pyonms.models.event import Event, EventParameter, Severity
from pyonms.models.node import ServiceType
from pyonms.utils import convert_time


@dataclass(repr=False)
class Alarm:
    id: int
    reductionKey: str
    type: int
    severity: Severity
    description: str
    logMessage: str
    uei: str = None
    location: str = None
    suppressedUntil: datetime = None
    suppressedTime: datetime = None
    x733ProbableCause: int = None
    affectedNodeCount: int = None
    count: int = None
    firstEventTime: datetime = None
    lastEventTime: datetime = None
    nodeId: int = None
    nodeLabel: str = None
    ipAddress: str = None
    ifIndex: int = None
    clearKey: str = None
    ackUser: str = None
    ackTime: int = None
    stickyMemo: str = None
    reductionKeyMemo: str = None
    troubleTicket: str = None
    troubleTicketLink: str = None
    troubleTicketState: int = None
    qosAlarmState: str = None
    managedObjectInstance: str = None
    managedObjectType: str = None
    label: str = None
    lastAutomationTime: datetime = None
    firstEvent: Optional[Event] = None
    lastEvent: Optional[Event] = None
    parameters: List[Optional[EventParameter]] = field(default_factory=list)
    relatedAlarms: Optional[List["Alarm"]] = field(default_factory=list)
    serviceType: ServiceType = None

    def __post_init__(self):
        self.suppressedUntil = convert_time(self.suppressedUntil)
        self.suppressedTime = convert_time(self.suppressedTime)
        self.firstEventTime = convert_time(self.firstEventTime)
        self.lastEventTime = convert_time(self.lastEventTime)
        self.lastAutomationTime = convert_time(self.lastAutomationTime)
        self.ackTime = convert_time(self.ackTime)
        self.severity = Severity[self.severity]
        if self.lastEvent:
            self.lastEvent = Event(**self.lastEvent)
        self.parameters = [EventParameter(**parameter) for parameter in self.parameters]
        if self.serviceType:
            self.serviceType = ServiceType(**self.serviceType)
        if self.relatedAlarms:
            relations = []
            for related in self.relatedAlarms:
                relations.append(Alarm(**related))
            self.relatedAlarms = relations

    def __repr__(self):
        return f"Alarm(id={self.id}, reductionKey={self.reductionKey})"
