# models.alarm.py

"Alarm models"

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from pyonms.models.event import Event, EventParameter, Severity
from pyonms.models.node import ServiceType
from pyonms.utils import convert_time


@dataclass(repr=False)
class Alarm:
    "Alarm model"
    id: int
    reductionKey: str
    type: int
    severity: Severity
    description: str
    logMessage: str
    uei: Optional[str] = None
    location: Optional[str] = None
    suppressedUntil: Optional[datetime] = None
    suppressedTime: Optional[datetime] = None
    x733ProbableCause: Optional[int] = None
    affectedNodeCount: Optional[int] = None
    count: Optional[int] = None
    firstEventTime: Optional[datetime] = None
    lastEventTime: Optional[datetime] = None
    nodeId: Optional[int] = None
    nodeLabel: Optional[str] = None
    ipAddress: Optional[str] = None
    ifIndex: Optional[int] = None
    clearKey: Optional[str] = None
    ackUser: Optional[str] = None
    ackTime: Optional[int] = None
    stickyMemo: Optional[str] = None
    reductionKeyMemo: Optional[str] = None
    troubleTicket: Optional[str] = None
    troubleTicketLink: Optional[str] = None
    troubleTicketState: Optional[int] = None
    qosAlarmState: Optional[str] = None
    managedObjectInstance: Optional[str] = None
    managedObjectType: Optional[str] = None
    label: Optional[str] = None
    firstAutomationTime: Optional[datetime] = None
    lastAutomationTime: Optional[datetime] = None
    firstEvent: Optional[Event] = None
    lastEvent: Optional[Event] = None
    parameters: List[Optional[EventParameter]] = field(default_factory=list)
    relatedAlarms: List[Optional["Alarm"]] = field(default_factory=list)
    serviceType: Optional[ServiceType] = None

    def __post_init__(self):
        self.suppressedUntil = convert_time(self.suppressedUntil)
        self.suppressedTime = convert_time(self.suppressedTime)
        self.firstEventTime = convert_time(self.firstEventTime)
        self.lastEventTime = convert_time(self.lastEventTime)
        self.firstAutomationTime = convert_time(self.firstAutomationTime)
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
