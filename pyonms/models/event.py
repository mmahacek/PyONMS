# models.event.py


from enum import Enum
from typing import Union
from dataclasses import dataclass, field

from pyonms.models.node import ServiceType
from pyonms.utils import convert_time


class Severity(Enum):
    INDETERMINATE = 1
    CLEARED = 2
    NORMAL = 3
    WARNING = 4
    MINOR = 5
    MAJOR = 6
    CRITICAL = 7


@dataclass
class EventParameter:
    name: str
    value: Union[int, str]
    type: str


@dataclass(repr=False)
class Event:
    id: int
    uei: str
    label: str
    time: int
    source: str
    createTime: int
    description: str
    logMessage: str
    severity: str
    log: str
    display: str
    location: str
    nodeId: int = None
    nodeLabel: str = None
    ipAddress: str = None
    host: str = None
    parameters: dict = field(default_factory=dict)
    serviceType: dict = field(default_factory=dict)

    def __post_init__(self):
        self.time = convert_time(self.time)
        self.createTime = convert_time(self.createTime)
        self.severity = Severity[self.severity]
        if self.display == "Y":
            self.display = True
        elif self.display == "N":
            self.display = False
        if self.log == "Y":
            self.log = True
        elif self.log == "N":
            self.log = False
        self.parameters = [EventParameter(**parameter) for parameter in self.parameters]
        if self.serviceType:
            self.serviceType = ServiceType(**self.serviceType)

    def __repr__(self):
        return f"Event(id={self.id}, uei={self.uei})"
